import datetime as dt

import sqlalchemy as sa
import sqlmodel as sm
from sqlalchemy.engine import Connection

from app.api.deps import SessionDep
from app.models import Product
from app.tables import t_tow

select_tow = sa.lambda_stmt(
    lambda: sa.select(t_tow.c["kod", "kod_p", "naz", "naz_p", "kod_k"]).where(
        t_tow.c.sta == "T",
        t_tow.c.akt == "T",
        t_tow.c.wsk_kuch.in_(["S", "T", "K", "X", "D"]),
    )
)


def sync_data(
    session: SessionDep,
    conn: Connection,
    remote_stmt: sa.LambdaElement,
    fir_code: str,
    parameters: dict = None,
):
    for row in conn.execute(remote_stmt, parameters=parameters):
        product = session.exec(
            sm.select(Product).where(Product.code == row.kod)
        ).one_or_none()
        if product:
            if product.price_updated_at < dt.date.today():
                cen = conn.execute(
                    sa.func.daj_cen_br(
                        row.kod, get_product_price(conn, row.kod, fir_code.upper())
                    )
                ).scalar()
                print(f"aktualizuje {row.kod_p}")
                product.price = cen
                product.price_updated_at = dt.date.today()
                session.add(product)
        else:
            cen = conn.execute(
                sa.func.daj_cen_br(
                    row.kod, get_product_price(conn, row.kod, fir_code.upper())
                )
            ).scalar()
            print(f"dodaje {row.kod_p}")
            product = Product(
                code=row.kod,
                name=row.naz,
                index=row.kod_p,
                full_name=row.naz_p,
                price=cen,
            )
            session.add(product)
        session.commit()


def get_product_price(
    conn: Connection, code: str, fir_code: str, kh_code: str = "000000"
):
    cursor = conn.connection.cursor()

    params = [
        fir_code,
        code,
        kh_code,
        dt.datetime.now(),
        "PLN",
        "B1",
        0,
        cursor.var(str),
        cursor.var(float),
        cursor.var(str),
        cursor.var(float),
        cursor.var(str),
        cursor.var(float),
        cursor.var(str),
        cursor.var(float),
        None,
        None,
        None,
        None,
        None,
        None,
        cursor.var(str),
        cursor.var(str),
        cursor.var(str),
        cursor.var(str),
        cursor.var(str),
    ]

    x = cursor.callfunc("meblecom.getcen.getcen", float, params)

    cursor.close()

    return x


def get_product(session: SessionDep, conn: Connection, code: str, fir_code: str):
    code = code.upper()
    local_stmt = sm.select(Product).where(Product.code == code)
    local_data = session.exec(local_stmt).all()
    local_data_codes = {row.code for row in local_data}
    local_data_codes = set(local_data_codes) or set()

    local_data_outdated = {
        row.code
        for row in local_data
        if row.price_updated_at
        < dt.datetime.combine(dt.date.today(), dt.datetime.min.time())
    } or set()

    remote_stmt = select_tow
    remote_stmt += lambda s: s.where(
        sa.and_(
            sa.and_(
                sa.or_(
                    t_tow.c.kod == code,
                    t_tow.c.tow_kod_pg == code,
                ),
                ~t_tow.c.kod.in_(local_data_codes),
            ),
            sa.or_(
                t_tow.c.kod.in_(local_data_outdated),
            ),
        )
    )

    sync_data(
        session,
        conn,
        remote_stmt=remote_stmt,
        fir_code=fir_code,
        parameters={"b_kod": code.upper()},
    )

    return session.exec(local_stmt).one_or_none()


def get_products_by_name(
    session: SessionDep,
    conn: Connection,
    name: str,
    fir_code: str,
    offset: int = 0,
    limit: int = 25,
):
    local_stmt = (
        sm.select(Product)
        .where(*[Product.name.icontains(n.strip()) for n in name.strip().split(" ")])
        .offset(offset)
        .limit(limit)
    )
    local_data = session.exec(local_stmt).all()

    local_data_codes = set({row.code for row in local_data}) if local_data else []

    remote_where = sa.and_(
        sa.or_(
            *[t_tow.c.naz.icontains(n.strip()) for n in name.strip().split(" ")],
            t_tow.c.kod.in_(local_data_codes),
        )
    )

    remote_stmt = select_tow
    remote_stmt += lambda s: s.where(remote_where).offset(offset).limit(limit)

    sync_data(
        session,
        conn,
        remote_stmt=remote_stmt,
        fir_code=fir_code,
    )

    return session.exec(local_stmt).all()
