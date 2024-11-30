from sqlmodel import Session

from app.models import OrderItem, OrderItemCreate


def create_order_item(*, session: Session, order_item_in: OrderItemCreate) -> OrderItem:
    order_item = OrderItem.model_valedate(order_item_in)
    session.add(order_item)
    session.commit()
    session.refresh(order_item)
    return order_item


def read_order_item(*, session: Session, order_item_id: int) -> OrderItem:
    order_item = session.get(OrderItem, order_item_id)
    return order_item
