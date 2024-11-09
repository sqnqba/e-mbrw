from backend.app.tests.utils.user import create_random_user
from backend.app.tests.utils.utils import random_lower_string, random_oso_kod
from sqlmodel import Session
from app.crud import order as crud

from app import create_order
from app.models import OrderCreate



def test_create_order(db: Session) -> None:
    user = create_random_user(db)
    owner_id = user.id
    assert owner_id is not None
    kh_kod = random_oso_kod()
    description = random_lower_string()
    order_in = OrderCreate(kh_kod=kh_kod, description=description)
    order = crud.create_order(session=db, order_in=order_in, owner_id=owner_id)
    assert order.kh_kod == kh_kod
    assert order.description == description
    assert order.owner_id == owner_id