import random
import string

from fastapi.testclient import TestClient

from app.core.config import settings


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_oso_kod() -> str:
    return "".join(random.choices(string.digits, k=6))


def random_value() -> float:
    return round(random.randint(0, 10000) / 100, 2)


def random_fir_kod() -> str:
    return f'S{"".join(random.choices(string.digits, k=2))}{random.choice(string.ascii_uppercase)}'


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def get_superuser_token_headers(client: TestClient) -> dict[str, str]:
    login_data = {
        "username": settings.FIRST_SUPERUSER_ORA_ID,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers
