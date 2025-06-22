from flask import Flask
from app.core.config import Config
from pathlib import Path



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.config['BABEL_TRANSLATION_DIRECTORIES'] = str(Path(Path(__file__).parent, 'translations'))


    # Initialize extensions
    from app.extensions import db, babel, get_locale
    db.init_app(app)
    babel.init_app(app, locale_selector=get_locale) # type: ignore

    # Register blueprints
    from app.views import register_blueprints
    register_blueprints(app)

    return app
