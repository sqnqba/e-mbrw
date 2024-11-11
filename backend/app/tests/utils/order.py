from sqlmodel import Session

from app.crud import order as crud
from app.models import Order, OrderCreate, User
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string, random_oso_kod


def create_random_order(db: Session, owner: User | None = None) -> Order:
    if owner is None:
        owner = create_random_user(db)
        assert owner is not None
    owner_id = owner.id
    kh_kod = random_oso_kod()
    fir_kod = owner.fir_kod
    description = random_lower_string()
    order_in = OrderCreate(kh_kod=kh_kod, fir_kod=fir_kod, description=description)
    return crud.create_order(session=db, order_in=order_in, owner_id=owner_id)
