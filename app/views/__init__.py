from flask import Flask
from .main import main as main_blueprint


def register_blueprints(app: Flask):
    """Register all blueprints for the application."""
    app.register_blueprint(main_blueprint)
