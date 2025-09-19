from flask_restx import reqparse
import re
from werkzeug.exceptions import BadRequest
from werkzeug.datastructures import FileStorage


add_product_parser = reqparse.RequestParser(bundle_errors=True)
add_product_parser.add_argument("category_id", type=str, location="form")
add_product_parser.add_argument("product_name", type=str, location="form")
add_product_parser.add_argument("description", type=str, location="form")
add_product_parser.add_argument("price", type=str, location="form")
add_product_parser.add_argument("image", type=FileStorage, location="files", required=False)


get_product_parser = reqparse.RequestParser(bundle_errors=True)
get_product_parser.add_argument(
    'access-token', type=str, required=True, location='headers')
get_product_parser.add_argument("product_id", type=str, location="form", required=False)


add_category_parser = reqparse.RequestParser(bundle_errors=True)
add_category_parser.add_argument("category_name", type=str, location="form", required=False)
add_category_parser.add_argument("category_parent_id", type=str, location="form", required=False)


add_variant_parser = reqparse.RequestParser(bundle_errors=True)
add_variant_parser.add_argument("product_id", type=str, location="json")
add_variant_parser.add_argument("variant_attributes", type=str, location="json")
add_variant_parser.add_argument("price", type=str, location="json")
add_variant_parser.add_argument("stock_quantity", type=str, location="json")
add_variant_parser.add_argument("variant_code", type=str, location="json")
