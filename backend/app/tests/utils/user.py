from app.core.config import settings
from app.crud import user as crud
from app.models import User, UserCreate, UserUpdate
from app.tests.utils.utils import (
    random_email,
    random_fir_kod,
    random_lower_string,
    random_oso_kod,
)
from fastapi.testclient import TestClient
from sqlmodel import Session


def user_authentication_headers(
    *, client: TestClient, email: str, password: str
) -> dict[str, str]:
    data = {"username": email, "password": password}

    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def create_random_user(db: Session) -> User:
    email = random_email()
    password = random_lower_string()
    oso_kod = random_oso_kod()
    fir_kod = random_fir_kod()
    user_in = UserCreate(
        email=email, password=password, oso_kod=oso_kod, fir_kod=fir_kod
    )
    user = user.create_user(session=db, user_create=user_in)
    return user


def authentication_token_from_email(
    *, client: TestClient, email: str, db: Session
) -> dict[str, str]:
    """
    Return a valid token for the user with given email.

    If the user doesn't exist it is created first.
    """
    password = random_lower_string()
    user = user.get_user_by_email(session=db, email=email)
    if not user:
        user_in_create = UserCreate(email=email, password=password)
        user = user.create_user(session=db, user_create=user_in_create)
    else:
        user_in_update = UserUpdate(password=password)
        if not user.id:
            raise Exception("User id not set")
        user = user.update_user(session=db, db_user=user, user_in=user_in_update)

    return user_authentication_headers(client=client, email=email, password=password)
