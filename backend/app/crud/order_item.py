from sqlmodel import Session, select

from app.models import OrderItem, OrderItemCreate


def create_order_item(*, session: Session, order_item_in: OrderItemCreate) -> OrderItem:
    order_item = OrderItem.model_validate(order_item_in)
    session.add(order_item)
    session.commit()
    session.refresh(order_item)
    return order_item


def read_order_items(*, session: Session, order_item_id: int) -> list[OrderItem]:
    order_items = session.exec(
        select(OrderItem).where(OrderItem.order_id == order_item_id)
    ).all()
    return order_items
