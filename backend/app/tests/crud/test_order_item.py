from random import random

from sqlmodel import Session

from app.crud import order_item as crud
from app.tests.utils.order import create_random_order
from app.tests.utils.order_item import create_random_order_item
from app.tests.utils.user import create_random_user


def test_create_order_item(db: Session) -> None:
    user = create_random_user(db)
    assert user is not None
    order = create_random_order(db, user)
    assert order is not None
    quantity = random.randint(1, 10)
    product_id = random.randint(1, 10)
    order_item_in = {
        "order_id": order.id,
        "product_id": product_id,
        "quantity": quantity,
    }

    crud.create_order_item(session=db, order_item_in=order_item_in)

    order_item = crud.read_order_item(session=db, order_item_id=1)

    assert order_item is not None
    assert order_item.order_id == order.id
    assert order_item.product_id == product_id
    assert order_item.quantity == quantity


def test_read_order_order_item(db: Session) -> None:
    user = create_random_user(db)
    assert user is not None
    order = create_random_order(db, user)
    assert order is not None
    order_item = create_random_order_item(db, order)
    assert order_item is not None
    assert order_item.order_id == order.id
    assert order_item.product_id == order_item.product_id
    assert order_item.quantity == order_item.quantity

    pass


# def test_update_order_item(db: Session) -> None:
#     pass


# def test_delete_order_item(db: Session) -> None:
#     pass


# def test_create_order_item_product_not_exist(db: Session) -> None:
#     pass
