
        

from store_application.models.store_model import Product, Category, Variant
from store_application.db_session import ScopedSession
import logging


def add_category(category_name, parent_id):
    local_session = ScopedSession()
    try:
        category = Category(
            name=category_name,
            parent_id=parent_id
        )

        local_session.add(category)
        local_session.commit()
        local_session.close()

        return True, "Category added successfully"

    except Exception as e:
        logging.error("validation error", exc_info=e)
        return False, "Unable to add the Category"



def add_product(category_id, product_name, description, price, image):
    local_session = ScopedSession()
    try:
        image_url = None
        if image and image.filename != '':
            """
            we can integrate S3 bucket or Cloudinary or other file storage options here
            and will store the url in product table
            """
            pass   
           

        product = Product(
            category_id = category_id ,
            name=product_name,
            description=description,
            price=price,
            image="https://res.cloudinary.com/dnwiknusf/image/upload/v1/blog_images/Screenshot_2025-02-18_at_3",  # for now using default Image URL
            mimetype="image/png"
        )

        local_session.add(product)
        local_session.commit()
        local_session.close()

        return True, "Product added successfully"

    except Exception as e:
        logging.error("validation error", exc_info=e)
        return False, "Unable to add the product"



def add_variant(product_id, variant_attributes, price, quantity, variant_code):
    local_session = ScopedSession()
    try:
        variant = Variant(
            product_id=product_id,
            variant_attributes=variant_attributes,
            price=price,
            stock_quantity=quantity,
            variant_code=variant_code
        )
        local_session.add(variant)
        local_session.commit()
        local_session.close()

        return True, "Variant added successfully"

    except Exception as e:
        logging.error("validation error", exc_info=e)
        return False, "Unable to add the Variant"