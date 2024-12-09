from typing import Any

from fastapi import APIRouter, HTTPException

from app.api.deps import OracleConnDep
from app.crud import product as crud
from app.models import SafoProduct

router = APIRouter()


@router.get("/{code}", response_model=SafoProduct)
def read_client(
    conn: OracleConnDep,
    # current_user: CurrentUser,
    code: str,
) -> Any:
    product = crud.get_product(conn=conn, code=code)
    if not product:
        raise HTTPException(status_code=404, detail="Brak produktu o podanym kodzie")
    return product._mapping
