from flask_sqlalchemy import SQLAlchemy
from flask import request
from flask_babel import Babel
from flask_login import LoginManager


def get_locale():
    language = request.accept_languages.best_match(['en','fr'])
    print(f"Selected Language: {language}"  )
    return language

db = SQLAlchemy()
babel = Babel()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
