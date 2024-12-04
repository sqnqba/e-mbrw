from typing import Any

from fastapi import APIRouter, HTTPException

from app.api.deps import CurrentUser, OracleConnDep
from app.crud import client as crud
from app.models import Client, Clients

router = APIRouter()


@router.get("/{code}", response_model=Client)
def read_client(
    conn: OracleConnDep,
    current_user: CurrentUser,
    code: str,
) -> Any:
    client = crud.get_client(conn=conn, code=code, fir_code=current_user.fir_kod)
    if not client:
        raise HTTPException(status_code=404, detail="Brak klienta o podanym kodzie")
    return client._mapping


@router.get("", response_model=Clients)
def find_kh(
    conn: OracleConnDep,
    current_user: CurrentUser,
    name: str | None = None,
    nip: str | None = None,
) -> Any:
    clients = crud.get_client_by_name_nip(
        conn=conn, name=name, nip=nip, fir_code=current_user.fir_kod
    )

    return {"data": [client._mapping for client in clients], "count": len(clients)}
