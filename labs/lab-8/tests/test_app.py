def test_home_page(client):
    """Test that home page loads"""
    response = client.get('/')
    assert response.status_code == 200

def test_login_page(client):
    """Test that home page loads"""
    response = client.get('/login')
    assert response.status_code == 200

def test_users_page(client):
    """Test that users page loads"""
    response = client.get('/users')
    assert response.status_code == 200

def test_invalid_first_name(client):
    """Test signup validation for invalid first name"""
    response = client.post('/signup', data={
        'FirstName': '123',  # invalid - contains numbers
        'LastName': 'Doe',
        'Email': 'test@test.com',
        'PhoneNumber': '1234567890',
        'Password': 'password123'
    })
    assert b'First name can only contain letters' in response.data

def test_invalid_phone_number(client):
    """Test signup validation for invalid phone number"""
    response = client.post('/signup', data={
        'FirstName': 'John',
        'LastName': 'Doe',
        'Email': 'test@test.com',
        'PhoneNumber': '123',  # invalid - not 10 digits
        'Password': 'password123'
    })
    assert b'Phone number must be exactly 10 digits' in response.data

# Additional test cases:
def test_invalid_last_name(client):
    """Test signup validation for invalid last name"""
    response = client.post('/signup', data={
        'FirstName': 'John',
        'LastName': '123', # invalid - contains numbers
        'Email': 'test@test.com',
        'PhoneNumber': '1234567890',
        'Password': 'password123'
    })
    assert b'Last name can only contain letters' in response.data

def test_signup_page_redirection(client):
    """Test that valid signup properly redirects user"""
    response = client.post('/signup', data={
        'FirstName': 'John',
        'LastName': 'Doe',
        'Email': 'test@test.com',
        'PhoneNumber': '1234567890',
        'Password': 'password123'
    })
    assert response.status_code == 302

def test_links_on_homepage(client):
    """Test if home page contains a links to other page"""
    response = client.get('/')
    assert b'Sign up!' in response.data and b'Log In!' in response.data and b'Users!' in response.data

def test_user_registration(client, monkeypatch, caplog):
    """Test if user registration information is inserted into db"""
    called = {}
    def test_insert(user):
        called['user'] = user
    
    import app
    monkeypatch.setattr(app, "insert", test_insert)
    with caplog.at_level("INFO"):
        response = client.post('/signup', data={
            'FirstName': 'Jane',
            'LastName': 'Doe',
            'Email': 'JaneDoe@test.com',
            'PhoneNumber': '1234567890',
            'Password': 'password123'
        })
    assert 'user' in called
    user_obj = called['user']
    assert user_obj.Email == 'JaneDoe@test.com'
    assert user_obj.FirstName == 'Jane'
    assert user_obj.LastName == 'Doe'
    assert "New user registered: JaneDoe@test.com" in caplog.text

def test_user_login(client, caplog):
    """Test user login with credentials"""
    client.post('/signup', data={
        'FirstName': 'Jon',
        'LastName': 'Doe',
        'Email': 'JonDoe@test.com',
        'PhoneNumber': '1234567890',
        'Password': 'password123'
    })
    with caplog.at_level("INFO"):
        response = client.post('/login', data={
            'Email': 'JonDoe@test.com',
            'Password': 'password123'
        })
    assert response.status_code == 302
    assert "Successful login: JonDoe@test.com" in caplog.text