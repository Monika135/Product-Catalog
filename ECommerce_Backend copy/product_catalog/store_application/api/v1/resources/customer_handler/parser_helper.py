from flask_restx import reqparse

products_query_parser = reqparse.RequestParser(bundle_errors=True)
products_query_parser.add_argument("category", type=str, required=False, location="args")
products_query_parser.add_argument("query", type=str, required=False, location="args")

cart_post_parser = reqparse.RequestParser(bundle_errors=True)
cart_post_parser.add_argument("variant_id", type=str, required=True, location="form")
cart_post_parser.add_argument("quantity", type=int, required=False, default=1, location="form")

cart_put_parser = reqparse.RequestParser(bundle_errors=True)
cart_put_parser.add_argument("quantity", type=int, required=True, location="form")

orders_post_parser = reqparse.RequestParser(bundle_errors=True)
orders_post_parser.add_argument("user_id", type=str, required=True, location="form")
