import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.tests.utils.order import create_random_order


def test_create_order(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {"kh_kod": "FooBar", "description": "Fighters"}
    response = client.post(
        f"{settings.API_V1_STR}/orders/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["kh_kod"] == data["kh_kod"]
    assert content["description"] == data["description"]
    assert "id" in content
    assert "owner_id" in content


def test_read_order(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    order = create_random_order(db)
    response = client.get(
        f"{settings.API_V1_STR}/orders/{order.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["kh_kod"] == order.kh_kod
    assert content["description"] == order.description
    assert content["id"] == str(order.id)
    assert content["owner_id"] == str(order.owner_id)


def test_read_order_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/orders/{uuid.uuid4()}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Order not found"


def test_read_order_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    order = create_random_order(db)
    response = client.get(
        f"{settings.API_V1_STR}/orders/{order.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_read_orders(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    create_random_order(db)
    create_random_order(db)
    response = client.get(
        f"{settings.API_V1_STR}/orders/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) >= 2


def test_update_order(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    order = create_random_order(db)
    data = {"kh_kod": "XXXXXX", "description": "Updated description"}
    response = client.put(
        f"{settings.API_V1_STR}/orders/{order.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["kh_kod"] == data["kh_kod"]
    assert content["description"] == data["description"]
    assert content["id"] == str(order.id)
    assert content["owner_id"] == str(order.owner_id)


def test_update_order_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {"kh_kod": "XXXXXX", "description": "Updated description"}
    response = client.put(
        f"{settings.API_V1_STR}/orders/{uuid.uuid4()}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Order not found"


def test_update_order_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    order = create_random_order(db)
    data = {"kh_kod": "XXXXXX", "description": "Updated description"}
    response = client.put(
        f"{settings.API_V1_STR}/orders/{order.id}",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_delete_order(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    order = create_random_order(db)
    response = client.delete(
        f"{settings.API_V1_STR}/orders/{order.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["message"] == "Order deleted successfully"


def test_delete_order_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    response = client.delete(
        f"{settings.API_V1_STR}/orders/{uuid.uuid4()}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Order not found"


def test_delete_order_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    order = create_random_order(db)
    response = client.delete(
        f"{settings.API_V1_STR}/orders/{order.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"
