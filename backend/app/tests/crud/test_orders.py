from fastapi.encoders import jsonable_encoder
from sqlmodel import Session

from app import create_order
from app.models import OrderCreate


def test_create_order(db: Session) -> None:
    pass