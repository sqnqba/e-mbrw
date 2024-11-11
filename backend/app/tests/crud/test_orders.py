from sqlmodel import Session, delete

from app.crud import order as crud
from app.models import Order, OrderCreate
from app.tests.utils.order import create_random_order
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_fir_kod, random_lower_string, random_oso_kod


def test_create_order(db: Session) -> None:
    user = create_random_user(db)
    owner_id = user.id
    assert owner_id is not None
    kh_kod = random_oso_kod()
    fir_kod = random_fir_kod()
    description = random_lower_string()
    order_in = OrderCreate(kh_kod=kh_kod, fir_kod=fir_kod, description=description)
    order = crud.create_order(session=db, order_in=order_in, owner_id=user.id)
    assert order.kh_kod == kh_kod
    assert order.fir_kod == fir_kod
    assert order.description == description
    assert order.owner_id == owner_id
    db.execute(delete(Order))
    db.commit()


def test_read_order(db: Session) -> None:
    user = create_random_user(db)
    assert user is not None
    random_order = create_random_order(db, user)
    order = crud.read_order(session=db, id=random_order.id)
    assert order.kh_kod == random_order.kh_kod
    assert order.fir_kod == random_order.fir_kod
    assert order.description == random_order.description
    db.execute(delete(Order))
    db.commit()


def test_read_all_orders(db: Session) -> None:
    count = 10
    for _ in range(count):
        create_random_order(db)

    orders, _ = crud.read_all_orders(session=db)
    assert len(orders) == count
    db.execute(delete(Order))
    db.commit()


def test_read_user_orders(db: Session) -> None:
    user = create_random_user(db)
    assert user is not None
    count = 10
    for _ in range(count):
        create_random_order(db)
        create_random_order(db, user)

    orders, _ = crud.read_user_orders(session=db, current_user=user)
    assert len(orders) == count
    db.execute(delete(Order))
    db.commit()


def test_read_fir_orders(db: Session) -> None:
    user_1 = create_random_user(db)
    assert user_1 is not None
    count_1 = 10
    for _ in range(count_1):
        create_random_order(db, user_1)

    user_2 = create_random_user(db)
    assert user_2 is not None

    count_2 = 5
    for _ in range(count_2):
        create_random_order(db, user_2)

    orders, _ = crud.read_fir_orders(session=db, fir_kod=user_1.fir_kod)
    assert len(orders) == count_1

    orders, _ = crud.read_fir_orders(session=db, fir_kod=user_2.fir_kod)
    assert len(orders) == count_2

    db.execute(delete(Order))
    db.commit()
