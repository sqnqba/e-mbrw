from app.crud import order as crud
from app.models import Order, OrderCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string, random_oso_kod
from sqlmodel import Session


def create_random_order(db: Session) -> Order:
    user = create_random_user(db)
    owner_id = user.id
    assert owner_id is not None
    kh_kod = random_oso_kod()
    description = random_lower_string()
    order_in = OrderCreate(kh_kod=kh_kod, description=description)
    return crud.create_order(session=db, order_in=order_in, owner_id=owner_id)
