from ...resources.Resource import APIResource
import logging
from flask_restx import Namespace, reqparse, ValidationError
from werkzeug.exceptions import BadRequest
from store_application.api.v1.decorators import require_auth
from flask_jwt_extended import get_jwt_identity
from flask import request
from .schema import (
    list_categories,
    list_products,
    add_to_cart,
    update_cart as update_cart_item,
    delete_cart as delete_cart_item,
    place_order as place_order_now,
)
from .parser_helper import (
    products_query_parser,
    cart_post_parser,
    cart_put_parser,
    orders_post_parser
)
api = Namespace('customer', description='Customer-facing operations')


class Categories(APIResource):
    def get(self):
        try:
            status, data = list_categories()
            if status:
                return {
                    "message": "Categories fetched successfully",
                    "data": data,
                    "status": True,
                    "type": "success_message"
                    }, 200

            return {
                "message": data,
                "status": False,
                "type": "custom_error"
                }, 400
        except Exception as e:
            logging.error("Categories_error", exc_info=e)
            return {"message": "Something went wrong", "status": False, "type": "custom_error"}, 400


class Products(APIResource):
    @api.expect(products_query_parser)
    def get(self):
        try:
            args = products_query_parser.parse_args()
            status, data = list_products(category_id=args.get("category"), q=args.get("query"))
            if status:
                return {
                    "message": "Products fetched successfully",
                    "data": data,
                    "status": True,
                    "type": "success_message"
                    }, 200

            return {
                "message": data,
                "status": False,
                "type": "custom_error"
                }, 400

        except (ValidationError, BadRequest) as e:
            return {"message": str(e), "status": False, "type": "validation_error"}, 400
        except Exception as e:
            logging.error("Products_error", exc_info=e)
            return {"message": "Something went wrong", "status": False, "type": "custom_error"}, 400


class Cart(APIResource):
    @require_auth
    @api.expect(cart_post_parser)
    def post(self):
        try:
            user_id = get_jwt_identity() 
            args = cart_post_parser.parse_args()
            status, data = add_to_cart(
                user_id=user_id,
                variant_id=args["variant_id"],
                quantity=args.get("quantity", 1),
            )
            if status:
                return {
                    "message": data.get("message"),
                    "item_id": data.get("id"),
                    "status": True,
                    "type": "success_message"
                    }, 201

            return {
                "message": data,
                "status": False,
                "type": "custom_error"
                }, 400

        except (ValidationError, BadRequest) as e:
            return {"message": str(e), "status": False, "type": "validation_error"}, 400
        except Exception as e:
            logging.error("Cart_error", exc_info=e)
            return {"message": "Something went wrong", "status": False, "type": "custom_error"}, 400

    @require_auth
    @api.expect(cart_put_parser)
    def put(self, item_id):
        try:
            args = cart_put_parser.parse_args()
            status, data = update_cart_item(item_id=item_id, quantity=args["quantity"])
            if status:
                return {
                    "message": data,
                    "status": True,
                    "type": "success_message"
                    }, 200

            return {
                "message": data,
                "status": False,
                "type": "custom_error"
                }, 400

        except (ValidationError, BadRequest) as e:
            return {"message": str(e), "status": False, "type": "validation_error"}, 400
        except Exception as e:
            logging.error("Cart PUT error", exc_info=e)
            return {"message": "Something went wrong", "status": False, "type": "custom_error"}, 400

    @require_auth
    def delete(self, item_id):
        try:
            status, data = delete_cart_item(item_id=item_id)
            if status:
                return {
                    "message": data, 
                    "status": True,
                    "type": "success_message"
                    }, 200
            return {
                "message": data,
                "status": False,
                "type": "custom_error"
                }, 400

        except Exception as e:
            logging.error("Cart DELETE error", exc_info=e)
            return {"message": "Something went wrong", "status": False, "type": "custom_error"}, 400


class Orders(APIResource):
    @require_auth
    @api.expect(orders_post_parser)
    def post(self):
        try:
            user_id = get_jwt_identity()
            status, data = place_order_now(user_id=user_id)
            if status:
                return {
                    "message": data.get("message"),
                    "order_id": data.get("order_id"),
                    "status": True,
                    "type": "success_message"
                    }, 201

            return {
                "message": data,
                "status": False,
                "type": "custom_error"
                }, 400

        except (ValidationError, BadRequest) as e:
            return {"message": str(e), "status": False, "type": "validation_error"}, 400
        except Exception as e:
            logging.error("Orders POST error", exc_info=e)
            return {"message": "Something went wrong", "status": False, "type": "custom_error"}, 400