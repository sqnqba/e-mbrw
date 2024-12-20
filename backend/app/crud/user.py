from typing import Any

from sqlmodel import Session, or_, select

from app.core.security import get_password_hash, verify_password
from app.models import User, UserCreate, UserUpdate


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str | None) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


def get_user_by_safo_credentials(*, session: Session, ora_id: str) -> User | None:
    statement = select(User).where(or_(User.ora_id == ora_id, User.oso_kod == ora_id))
    session_user = session.exec(statement).first()
    return session_user


def authenticate(*, session: Session, login: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=login)
    if not db_user:
        db_user = get_user_by_safo_credentials(session=session, ora_id=login)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user
