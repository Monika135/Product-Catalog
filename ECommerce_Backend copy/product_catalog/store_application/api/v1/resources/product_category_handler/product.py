from ...resources.Resource import (
    APIResource,
)
import logging
from flask_restx import Namespace
from .parser_helper import add_product_parser, add_category_parser, add_variant_parser
from .schema import add_product, add_category, add_variant
from store_application.api.v1.decorators import require_roles

api = Namespace('auth', description='Auth related operations')


class AdminProducts(APIResource):
    @require_roles("admin")
    @api.doc(security="BearerAuth")
    @api.expect(add_product_parser)
    def post(self):
        try:
            product_data = add_product_parser.parse_args()
            category_id = product_data["category_id"]
            product_name = product_data["product_name"]
            description = product_data["description"]
            price = product_data["price"]
            image = product_data["image"]
            status, data = add_product(category_id, product_name, description, price, image)
            if status:
                return {
                    "message": data,
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



class AdminCategory(APIResource):
    @require_roles("admin")
    @api.expect(add_category_parser)
    @api.doc(security="BearerAuth")
    def post(self):
        try:
            category_data = add_category_parser.parse_args()
            category_name = category_data["category_name"]
            parent_id = category_data["category_parent_id"]
            status, data = add_category(category_name, parent_id)
            if status:
                return {
                    "message": data,
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


class AdminVariant(APIResource):
    @require_roles("admin")
    @api.doc(security="BearerAuth")
    @api.expect(add_variant_parser)
    def post(self):
        try:
            variant_data = add_variant_parser.parse_args()
            product_id = variant_data["product_id"]
            variant_attributes = variant_data["variant_attributes"]
            price = variant_data["price"]
            quantity = variant_data["stock_quantity"]
            variant_code = variant_data["variant_code"]
            status, data = add_variant(product_id, variant_attributes, price, quantity, variant_code)
            if status:
                return {
                    "message": data,
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
