import os

class Config:
    """
    Configuration class for the application.
    """

    SECRET_KEY: str = os.getenv('SECRET_KEY', 'default_secret_key')
    SQLALCHEMY_DATABASE_URI: str = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    DEBUG: bool = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')
    
    # BABEL_DEFAULT_LOCALE: str = os.getenv('BABEL_DEFAULT_LOCALE', 'en')
