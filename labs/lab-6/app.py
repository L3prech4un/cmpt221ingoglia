"""app.py: render and route to webpages"""

import os
import re
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from db.query import get_all, insert, get_one
from db.server import init_database
from db.schema import Users 
import bcrypt
from jinja2 import Environment, PackageLoader, select_autoescape
import logging

# set up jinja environment
jinja_env = Environment(
    loader=PackageLoader("app"),
    autoescape=select_autoescape()
)

# load environment variables from .env
load_dotenv()

# database connection - values set in .env
db_name = os.getenv('db_name')
db_owner = os.getenv('db_owner')
db_pass = os.getenv('db_pass')
db_url = f"postgresql://{db_owner}:{db_pass}@localhost/{db_name}"

# Error logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(filename='logs/log.txt', level=logging.INFO, filemode='a', format="%(asctime)s - [%(levelname)s] - %(message)s")
logger = logging.getLogger(__name__)


def create_app():
    """Create Flask application and connect to your DB"""
    # create flask app
    app = Flask(__name__, 
                template_folder=os.path.join(os.getcwd(), 'templates'), 
                static_folder=os.path.join(os.getcwd(), 'static'))
    
    # connect to db
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    
    # Initialize database
    with app.app_context():
        if not init_database():
            print("Failed to initialize database. Exiting.")
            exit(1)

    # ===============================================================
    # routes
    # ===============================================================

    # create a webpage based off of the html in templates/index.html
    @app.route('/')
    def index():
        """Home page"""
        return render_template('index.html')
    
    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        """Sign up page: enables users to sign up"""
        form = {key: value.strip() for key, value in request.form.items()}
        if request.method == 'POST':
            isValid = False
            try:                
                if form['FirstName'].isalpha():
                    print(f'Input: {form["FirstName"]} is valid.')
                    isValid = True
                else:
                    isValid = False
                    print(f'Input: {form["FirstName"]} is not valid. First name can only contain letters.')
                    logger.error(f'Input: {form["FirstName"]} is not valid. First name can only contain letters.')
                    usr_error_msg = "First name can only contain letters."
                    return render_template('signup.html', error=usr_error_msg)

                if form['LastName'].isalpha():
                    print(f'Input: {form["LastName"]} is valid.')
                    isValid = True
                else:
                    isValid = False
                    print(f'Input: {form["LastName"]} is not valid')
                    logger.error(f'Input: {form["LastName"]} is not valid')
                    usr_error_msg = "Last name can only contain letters."
                    return render_template('signup.html', error=usr_error_msg)


                if form['PhoneNumber'].isnumeric and re.fullmatch(r'\d{10}', form["PhoneNumber"]):
                    print(f'Input: {form["PhoneNumber"]} is valid.')
                else:
                    isValid = False
                    print(f'Input: {form["PhoneNumber"]} is not valid. Please make sure it only contains numbers [0-9] and it 10 characters in length.')
                    logger.error(f'Input: {form["PhoneNumber"]} is not valid. Please make sure it only contains numbers [0-9] and it 10 characters in length.')
                    usr_error_msg = "Phone number must be 10 digits long and contain only numbers [0-9]."
                    return render_template('signup.html', error=usr_error_msg)

                if isValid:
                    user = Users(FirstName=form['FirstName'],
                            LastName=form['LastName'],
                            Email=form['Email'],
                            PhoneNumber=form['PhoneNumber'],
                            Password=form['Password'])
                    hashed = bcrypt.hashpw(user.Password.encode('utf-8'), bcrypt.gensalt())
                    user.Password = hashed.decode('utf-8')
                    try:    
                        insert(user)
                        return redirect(url_for('login'))
                    except Exception as e:
                        print(f"[ERROR] An error occured: {e}")
                        logger.error(f"[ERROR] An error occured: {e}")
                else:
                    usr_error_msg = "An error occurred while creating your account. Please try again later."
                    return render_template('error.html', error=usr_error_msg)
            except Exception as e:
                print("Error inserting user: ", e)
                logger.error("Error inserting user: ", e)

                usr_error_msg = "One or more of your inputs were invalid. Please try again."
                return render_template('error.html', error=usr_error_msg)
        elif request.method == 'GET':
            return render_template('signup.html')
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """Log in page: enables users to log in"""
        form = {key: value.strip() for key, value in request.form.items()}
        if request.method == 'POST':
            try:
                email = form['Email']
                password_entered = form['Password']
                user = get_one(Users, Email=email)

                if user and user.Password:
                    user_hash = user.Password.encode('utf-8')
                    if bcrypt.checkpw(password_entered.encode('utf-8'), user_hash):
                        print("Password do match!")
                        return redirect(url_for('success'))
                    else:
                        print("Passwords do not match!")
                        logger.info(f"Failed login attempt for {email}!\nPasswords did not match.")
                        return redirect('/login')
                else:
                    print("Email does not exist!")
                    logger.info(f"Failed login attempt for {email}!\nEmail does not exist.")
                    return redirect('/login')
            except Exception as e:
                print("Error Logging in: ", e)
                logger.error(f"An error occurred during login: {e} ")
                return redirect('/login')
        elif request.method == 'GET':
            return render_template('login.html')

    @app.route('/users')
    def users():
        """Users page: displays all users in the Users table"""
        all_users = get_all(Users)
        
        return render_template('users.html', users=all_users)

    @app.route('/success')
    def success():
        """Success page: displayed upon successful login"""

        return render_template('success.html')

    return app

if __name__ == "__main__":
    app = create_app()
    # debug refreshes your application with your new changes every time you save
    app.run(debug=True)