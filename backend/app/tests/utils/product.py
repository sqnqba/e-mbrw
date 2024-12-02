import random

from sqlmodel import Session

from app.models import Product, ProductCreate
from app.tests.utils.utils import random_lower_string


def create_random_product(session: Session) -> Product:
    product_in = ProductCreate(
        name=random_lower_string(),
        price=random.randint(1, 10),
        description=random_lower_string(),
    )
    product = Product.model_validate(product_in)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product
