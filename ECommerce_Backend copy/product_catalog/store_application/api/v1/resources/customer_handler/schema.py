import logging
from store_application.db_session import ScopedSession
from store_application.models.store_model import (
    Category, Product, Variant,
    UserProductMapping, Orders, OrderItem
)


def list_categories():
    local_session = ScopedSession()
    try:
        categories = local_session.query(Category).all()
        data = [{"id": str(c.id), "name": c.name, "parent_id": str(c.parent_id)} for c in categories]
        local_session.close()
        return True, data
    except Exception as e:
        logging.error("list_categories error", exc_info=e)
        return False, "Unable to fetch categories"


def list_products(category_id=None, q=None):
    local_session = ScopedSession()
    try:
        query = local_session.query(Product)
        if category_id:
            query = query.filter(Product.category_id == category_id)
        if q:
            query = query.filter(Product.name.ilike(f"%{q}%"))
        products = query.all()
        data = [{"id": str(p.id), "name": p.name, "price": p.price, "category_id": str(p.category_id)} for p in products]
        local_session.close()
        return True, data
    except Exception as e:
        logging.error("list_products error", exc_info=e)
        return False, "Unable to fetch products"


def add_to_cart(user_id, variant_id, quantity=1):
    local_session = ScopedSession()
    try:
        # If item already in cart, increment quantity
        item = (
            local_session.query(UserProductMapping)
            .filter(
                UserProductMapping.user_id == user_id,
                UserProductMapping.variant_id == variant_id,
            )
            .first()
        )
        if item:
            item.quantity = item.quantity + int(quantity)
        else:
            item = UserProductMapping(
                user_id=user_id, variant_id=variant_id, quantity=int(quantity)
            )
            local_session.add(item)

        local_session.commit()
        item_id = str(item.id)
        local_session.close()
        return True, {"message": "Added to cart", "id": item_id}
    except Exception as e:
        logging.error("add_to_cart error", exc_info=e)
        return False, "Unable to add to cart"


def update_cart(item_id, quantity):
    local_session = ScopedSession()
    try:
        item = local_session.query(UserProductMapping).get(item_id)
        if not item:
            local_session.close()
            return False, "Cart item not found"

        item.quantity = int(quantity)
        local_session.commit()
        local_session.close()
        return True, "Cart updated"
    except Exception as e:
        logging.error("update_cart error", exc_info=e)
        return False, "Unable to update cart"


def delete_cart(item_id):
    local_session = ScopedSession()
    try:
        item = local_session.query(UserProductMapping).get(item_id)
        if not item:
            local_session.close()
            return False, "Cart item not found"

        local_session.delete(item)
        local_session.commit()
        local_session.close()
        return True, "Item removed"
    except Exception as e:
        logging.error("delete_cart error", exc_info=e)
        return False, "Unable to remove item"


def place_order(user_id):
    local_session = ScopedSession()
    try:
        cart_items = (
            local_session.query(UserProductMapping)
            .filter(UserProductMapping.user_id == user_id)
            .all()
        )
        if not cart_items:
            local_session.close()
            return False, "Cart is empty"

        total_price = 0.0
        for ci in cart_items:
            variant = local_session.query(Variant).get(ci.variant_id)
            if not variant:
                continue
            total_price += float(variant.price) * int(ci.quantity)

        order = Orders(user_id=user_id, total_price=total_price)
        local_session.add(order)
        local_session.flush()

        for ci in cart_items:
            variant = local_session.query(Variant).get(ci.variant_id)
            if not variant:
                continue
            order_item = OrderItem(
                order_id=order.id,
                variant_id=ci.variant_id,
                quantity=int(ci.quantity),
                price=float(variant.price),
            )
            local_session.add(order_item)
            local_session.delete(ci)

        local_session.commit()
        order_id = str(order.id)
        local_session.close()
        return True, {"message": "Order placed", "order_id": order_id, "total_amount": total_price}
    except Exception as e:
        logging.error("place_order error", exc_info=e)
        return False, "Unable to place order"