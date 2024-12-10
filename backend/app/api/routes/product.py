from typing import Any

from fastapi import APIRouter, HTTPException

from app.api.deps import CurrentUser, OracleConnDep, SessionDep
from app.crud import product as crud
from app.models import ProductPublic, ProductsPublic

router = APIRouter()


@router.get("", response_model=ProductsPublic)
def read_products(
    session: SessionDep,
    conn: OracleConnDep,
    current_user: CurrentUser,
    naz: str | None = None,
) -> Any:
    products = crud.get_products_by_name(
        session=session, conn=conn, name=naz, fir_code=current_user.fir_kod
    )
    return {"data": products, "count": len(products)}


@router.get("/{code}", response_model=ProductPublic)
def read_product(
    session: SessionDep,
    conn: OracleConnDep,
    current_user: CurrentUser,
    code: str,
) -> Any:
    product = crud.get_product(
        session=session, conn=conn, code=code, fir_code=current_user.fir_kod
    )
    if not product:
        raise HTTPException(status_code=404, detail="Brak produktu o podanym kodzie")
    return product
