import random

from sqlmodel import Session

from app.models import Order, OrderItem


def create_random_order_item(session: Session, order: Order) -> Order:
    quantity = random.randint(1, 10)
    product_id = random.randint(1, 10)
    order_item = OrderItem(order_id=order.id, product_id=product_id, quantity=quantity)

    session.add(order_item)
    session.commit()
    session.refresh(order_item)
    return order_item
