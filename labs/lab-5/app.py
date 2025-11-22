"""app.py: render and route to webpages"""

import os
from dotenv import load_dotenv
from flask import Flask, render_template
from db.server import init_database, get_session

# load environment variables from .env
load_dotenv()

# database connection - values set in .env
db_name = os.getenv('db_name')
db_owner = os.getenv('db_owner')
db_pass = os.getenv('db_pass')
db_url = f"postgresql://{db_owner}:{db_pass}@localhost/{db_name}"

def create_app():
    """Create Flask application and connect to your DB"""
    # create flask app
    app = Flask(__name__, 
                template_folder=os.path.join(os.getcwd(), 'labs/lab-5/templates'), 
                static_folder=os.path.join(os.getcwd(), 'labs/lab-5/static'))
    
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
    
    # add more routes here!
    @app.route('/brown.html')
    def brown():
        """Brown page"""
        return render_template('brown.html')
    
    @app.route('/about.html')
    def about():
        """About page"""
        return render_template('about.html')

    return app

if __name__ == "__main__":
    app = create_app()
    # debug refreshes your application with your new changes every time you save
    app.run(debug=True)