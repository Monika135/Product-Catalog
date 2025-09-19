from flask import Blueprint
from flask_restx import Api

v1_blueprint = Blueprint("v1", __name__)

authorizations = {
    "BearerAuth": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": 'JWT Authorization header using the Bearer scheme. Example: "Bearer <token>"'
    }
}


v1_api = Api(
    v1_blueprint,
    prefix="/v1",
    title="ECommerce Product Catalog",
    version="1.0",
    description="ECommerce Product Catalog API's",
    doc="/apidocs/",
)

from store_application.api.v1.resources.health_check import HealthCheck
from store_application.api.v1.resources.auth_handler.auth import Signup, Login, AdminSignup
from store_application.api.v1.resources.product_category_handler.product import AdminProducts, AdminCategory, AdminVariant
from store_application.api.v1.resources.customer_handler.customer_handler import Categories, Products, Cart, Orders

v1_api.add_resource(HealthCheck, "/health_check/")
v1_api.add_resource(Signup, "/user/signup/")
v1_api.add_resource(AdminSignup, "/admin/signup/")
v1_api.add_resource(Login, "/login/")
v1_api.add_resource(AdminProducts, "/admin/products/")
v1_api.add_resource(AdminCategory, "/admin/category/")
v1_api.add_resource(AdminVariant, "/admin/variant/")


# Customer routes
v1_api.add_resource(Categories, "/categories/")
v1_api.add_resource(Products, "/products/list/")
v1_api.add_resource(Cart, "/cart/", "/cart/<string:item_id>/")
v1_api.add_resource(Orders, "/orders/")