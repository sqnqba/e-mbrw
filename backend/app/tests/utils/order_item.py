import random

from sqlmodel import Session

from app.models import Order, OrderItem, Product
from app.tests.utils.order import create_random_order
from app.tests.utils.product import create_random_product


def create_random_order_item(
    session: Session, order: Order | None, product: Product | None
) -> OrderItem:
    if order is None:
        order = create_random_order(session)
    if product is None:
        product = create_random_product(session)

    quantity = random.randint(1, 10)
    order_item = OrderItem(order_id=order.id, product_id=product.id, quantity=quantity)

    session.add(order_item)
    session.commit()
    session.refresh(order_item)
    return order_item
