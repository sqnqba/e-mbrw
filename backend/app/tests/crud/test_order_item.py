import random

from sqlmodel import Session, delete

from app.crud import order_item as crud
from app.models import OrderItem, OrderItemUpdate
from app.tests.utils.order import create_random_order
from app.tests.utils.order_item import create_random_order_item
from app.tests.utils.product import create_random_product
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

    order_items = crud.read_order_items(session=db, order_item_id=order.id)

    assert len(order_items) > 0

    db.execute(delete(OrderItem))


def test_read_order_order_item(db: Session) -> None:
    user = create_random_user(db)
    assert user is not None
    order = create_random_order(db, user)
    assert order is not None
    product = create_random_product(db)
    assert product is not None
    order_item = crud.create_order_item(
        session=db,
        order_item_in={"order_id": order.id, "product_id": product.id, "quantity": 1},
    )
    assert order_item is not None
    assert order_item.order_id == order.id
    assert order_item.product_id == product.id
    assert order_item.quantity == 1

    db.delete(order_item)
    db.delete(product)
    db.delete(order)
    db.delete(user)

    db.commit()


def test_update_order_item(db: Session) -> None:
    user = create_random_user(db)
    assert user is not None
    order = create_random_order(db, user)
    assert order is not None
    product = create_random_product(db)
    assert product is not None
    order_item = create_random_order_item(db, order, product)
    assert order_item is not None

    new_product = create_random_product(db)
    quantity = random.randint(1, 10)
    order_item_in = OrderItemUpdate(
        product_id=new_product.id,
        quantity=quantity,
    )

    crud.update_order_item(
        session=db, order_item=order_item, order_item_in=order_item_in
    )
    db.refresh(order_item)
    assert order_item.order_id == order.id
    assert order_item.product_id == new_product.id
    assert order_item.quantity == quantity

    db.delete(order_item)
    db.delete(product)
    db.delete(new_product)
    db.delete(order)
    db.delete(user)


# def test_delete_order_item(db: Session) -> None:
#     pass
