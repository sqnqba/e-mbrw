import uuid
from typing import Any

from app.core.security import get_password_hash, verify_password
from app.models import Order, OrderCreate, User, UserCreate, UserUpdate
from sqlmodel import Session, or_, select


def create_order(
    *, session: Session, order_in: OrderCreate, owner_id: uuid.UUID
) -> Order:
    db_order = Order.model_validate(order_in, update={"owner_id": owner_id})
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order
