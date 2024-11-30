import random

from sqlmodel import Session, create_engine, select

from app.core.config import settings
from app.crud import user as user_crud
from app.models import Order, Product, User, UserCreate

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/fastapi/full-stack-fastapi-template/issues/28


def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqlmodel import SQLModel

    # This works because the models are already imported and registered from app.models
    # SQLModel.metadata.create_all(engine)

    user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER_EMAIL)
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER_EMAIL,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
            ora_id=settings.FIRST_SUPERUSER_ORA_ID,
            oso_kod=settings.FIRST_SUPERUSER_OSO_KOD,
            fir_kod=settings.FIRST_SUPERUSER_FIR_KOD,
        )
        user = user_crud.create_user(session=session, user_create=user_in)

    if settings.ENVIRONMENT == "local":
        order = Order(
            kh_kod="000000",
            kh_naz="test",
            owner_id=user.id,
        )
        session.add(order)
        session.commit()

        for i in range(10):
            product = Product(
                index=f"test{i}",
                price=random.randint(0, 1000) / 100,
                description=f"Test product {i}",
            )
            session.add(product)
        session.commit()
