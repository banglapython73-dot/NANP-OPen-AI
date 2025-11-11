import os
from flask import Flask
from ..config import config_by_name

def create_app(config_name='dev'):
    """Creates and configures the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Ensure the upload folder exists
    try:
        os.makedirs(app.config['UPLOAD_FOLDER'])
    except OSError:
        pass

    # Import and register blueprints here
    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
