import uuid
from typing import Any

from sqlmodel import Session, select

from app.models import OrderItem, OrderItemCreate, OrderItemUpdate


def create_order_item(*, session: Session, order_item_in: OrderItemCreate) -> OrderItem:
    order_item = OrderItem.model_validate(order_item_in)
    session.add(order_item)
    session.commit()
    session.refresh(order_item)
    return order_item


def read_order_items(*, session: Session, order_id: uuid.UUID) -> Any:
    order_items = session.exec(
        select(OrderItem).where(OrderItem.order_id == order_id)
    ).all()
    return order_items


def update_order_item(
    *, session: Session, order_item: OrderItem, order_item_in: OrderItemUpdate
) -> Any:
    order_item_data = order_item_in.model_dump(exclude_unset=True)
    order_item.sqlmodel_update(order_item_data)
    session.add(order_item)
    session.commit()
    session.refresh(order_item)
    return order_item


def delete_order_item(*, session: Session, order_item_id: int) -> None:
    order_item = session.get(OrderItem, order_item_id)
    session.delete(order_item)
    session.commit()
