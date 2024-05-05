from flask import Flask
from .routes import main  # Ensure this import is correct

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.register_blueprint(main)  # Make sure the Blueprint is registered
    return app