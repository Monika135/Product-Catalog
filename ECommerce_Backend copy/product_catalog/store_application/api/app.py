from flask import Flask, jsonify
from flask_cors import CORS
from .v1 import v1_blueprint
from flask_jwt_extended import JWTManager
import logging


def create_app():
    app = Flask(__name__)
    CORS(
        app,
        resources={r"/*": {"origins": "*", "send_wildcard": "False"}},
    )
    CORS(app)

    jwt = JWTManager(app)
    logging.info(jwt)

    app.register_blueprint(v1_blueprint)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
