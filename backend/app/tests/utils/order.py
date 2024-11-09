from app.crud import user as crud
from app.models import Order, OrderCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string
from sqlmodel import Session


def create_random_order(db: Session) -> Order:
    user = create_random_user(db)
    owner_id = user.id
    assert owner_id is not None
    title = random_lower_string()
    description = random_lower_string()
    order_in = OrderCreate(title=title, description=description)
    return crud.create_order(session=db, order_in=order_in, owner_id=owner_id)
