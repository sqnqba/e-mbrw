import uuid
from typing import Any

from fastapi import APIRouter, HTTPException

from app.api.deps import CurrentUser, SessionDep
from app.crud import order as crud
from app.models import (
    Message,
    Order,
    OrderCreate,
    OrderPublic,
    OrdersPublic,
    OrderUpdate,
)

router = APIRouter()


@router.post("/", response_model=OrderPublic)
def create_order(
    *, session: SessionDep, current_user: CurrentUser, order_in: OrderCreate
) -> Any:
    """
    Create new order.
    """
    return crud.create_order(
        session=session, order_in=order_in, owner_id=current_user.id
    )


@router.get("/{id}", response_model=OrderPublic)
def read_order(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Get order by ID.
    """
    order = crud.read_order(session=session, id=id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if not current_user.is_superuser and (order.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return order


@router.get("/", response_model=OrdersPublic)
def read_orders(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve orders.
    """

    if current_user.is_superuser:
        orders, count = crud.read_all_orders(session=session, skip=skip, limit=limit)
    else:
        orders, count = crud.read_user_orders(
            session=session, current_user=current_user, skip=skip, limit=limit
        )
    return OrdersPublic(data=orders, count=count)


@router.put("/{id}", response_model=OrderPublic)
def update_order(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    order_in: OrderUpdate,
) -> Any:
    """
    Update an order.
    """
    order = session.get(Order, id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if not current_user.is_superuser and (order.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    update_dict = order_in.model_dump(exclude_unset=True)
    order.sqlmodel_update(update_dict)
    session.add(order)
    session.commit()
    session.refresh(order)
    return order


@router.delete("/{id}")
def delete_order(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete an order.
    """
    order = session.get(Order, id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if not current_user.is_superuser and (order.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    session.delete(order)
    session.commit()
    return Message(message="Order deleted successfully")
