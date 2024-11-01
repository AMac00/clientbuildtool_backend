from flask import Flask
from flask_session import Session
from flask_pymongo import PyMongo
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restful import Resource, Api
# Import environment configurations
from env_config import ProductionConfig



"""Construct the core application."""
app = Flask(__name__, instance_relative_config=False)
app.config.from_object(ProductionConfig)  # Set globals
CORS(app)
api = Api(app)
with app.app_context():
    # Import Blueprints
    from views.bp_dev import bp_dev
    from views.bp_users import bp_users
    # Add blueprint to API
    api.init_app(bp_users)
    # Register Blueprints
    app.register_blueprint(bp_dev)
    app.register_blueprint(bp_users)


# Used for local testing
if __name__ == "__main__":
    app.run(host='0.0.0.0')

