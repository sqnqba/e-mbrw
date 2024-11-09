import uuid

from sqlmodel import Session

from app.models import Order, OrderCreate


def create_order(
    *, session: Session, order_in: OrderCreate, owner_id: uuid.UUID
) -> Order:
    db_order = Order.model_validate(order_in, update={"owner_id": owner_id})
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order
