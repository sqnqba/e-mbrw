import uuid
from collections.abc import Sequence

from sqlmodel import Session, func, select

from app.api.deps import CurrentUser
from app.models import Order, OrderCreate


def create_order(
    *, session: Session, order_in: OrderCreate, owner_id: uuid.UUID
) -> Order:
    db_order = Order.model_validate(order_in, update={"owner_id": owner_id})
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order


def read_order(*, session: Session, id: uuid.UUID) -> Order | None:
    return session.get(Order, id)


def read_all_orders(
    *, session: Session, skip: int = 0, limit: int = 100
) -> tuple[Sequence[Order], int]:
    count_stmt = select(func.count()).select_from(Order)
    count = session.exec(count_stmt).one()

    select_stmt = select(Order).offset(skip).limit(limit)
    orders = session.exec(select_stmt).all()
    return (orders, count)


def read_user_orders(
    *, session: Session, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> tuple[Sequence[Order], int]:
    count_stmt = (
        select(func.count()).select_from(Order).where(Order.owner_id == current_user.id)
    )
    count = session.exec(count_stmt).one()

    select_stmt = (
        select(Order).where(Order.owner_id == current_user.id).offset(skip).limit(limit)
    )
    orders = session.exec(select_stmt).all()
    return (orders, count)


def read_fir_orders(
    *, session: Session, fir_kod: str, skip: int = 0, limit: int = 100
) -> tuple[Sequence[Order], int]:
    count_stmt = select(func.count()).select_from(Order).where(Order.fir_kod == fir_kod)
    count = session.exec(count_stmt).one()

    select_stmt = (
        select(Order).where(Order.fir_kod == fir_kod).offset(skip).limit(limit)
    )
    orders = session.exec(select_stmt).all()
    return (orders, count)
