from ...resources.Resource import (
    APIResource,
)
import logging
from flask_restx import Namespace
from .parser_helper import signup_parser, StrongPasswordError, login_parser
from .schema import register_user, login_user
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import BadRequest, HTTPException
from flask_restx import ValidationError
api = Namespace('auth', description='Auth related operations')


class Signup(APIResource):
    @api.expect(signup_parser)
    def post(self):
        try:
            signup_data = signup_parser.parse_args()
            username = signup_data["username"]
            mobile = signup_data["mobile"]
            email = signup_data["email"]
            password = signup_data["password"]
            status, data = register_user(username, mobile, email, password)
            if status:
                return {
                    "message": "Account created successfully",
                    "data" : {
                        "user_id": str(data.id),
                        "username": data.username,
                        "email": data.email,
                        "phone": data.phone
                    },
                    "status": status,
                    "type": "success_message"
                }, 201
            else:
                return {
                    "message": data,
                    "status": status,
                    "type": "custom_error"
                }, 400

        except StrongPasswordError as e:
            return {
                "message": str(e),
                "status": False,
                "type": "validation_error"
            }, 400


        except Exception as e:
            logging.error(
                "Input validation error", exc_info=e
            )
            return {
                "message": "Something went wrong",
                "status": False,
                "type": "custom_error"
            }, 400
        

class Login(APIResource):
    @api.expect(login_parser)
    def post(self):
        try:
            login_data = login_parser.parse_args()
            email = login_data["email"]
            password = login_data["password"]
            status, data = login_user(email, password)
            if status:
                return {
                    "message": "User logged in successfully",
                    "tokens": data,
                    "status": status,
                    "type": "success_message"
                }, 201
            else:
                return {
                    "message": data,
                    "status": status,
                    "type": "custom_error"
                }, 400

        except Exception as e:
            logging.error(
                "Input validation error", exc_info=e
            )
            return {
                "message": "Something went wrong",
                "status": False,
                "type": "custom_error"
            }, 400


class AdminSignup(APIResource):
    @api.expect(signup_parser)
    def post(self):
        try:
            signup_data = signup_parser.parse_args()
            username = signup_data["username"]
            mobile = signup_data["mobile"]
            email = signup_data["email"]
            password = signup_data["password"]
            user_group = signup_data["user_group"]
            status, data = register_user(username, mobile, email, password, user_group)
            if status:
                return {
                    "message": "Account created successfully",
                    "data" : {
                        "user_id": str(data.id),
                        "username": data.username,
                        "email": data.email,
                        "phone": data.phone
                    },
                    "status": status,
                    "type": "success_message"
                }, 201
            else:
                return {
                    "message": data,
                    "status": status,
                    "type": "custom_error"
                }, 400

        except StrongPasswordError as e:
            return {
                "message": str(e),
                "status": False,
                "type": "validation_error"
            }, 400


        except Exception as e:
            logging.error(
                "Input validation error", exc_info=e
            )
            return {
                "message": "Something went wrong",
                "status": False,
                "type": "custom_error"
            }, 400