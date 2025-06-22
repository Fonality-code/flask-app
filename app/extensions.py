from flask_sqlalchemy import SQLAlchemy
from flask import request
from flask_babel import Babel


def get_locale():
    language = request.accept_languages.best_match(['en','fr'])
    print(f"Selected Language: {language}"  )
    return language

db = SQLAlchemy()
babel = Babel()
