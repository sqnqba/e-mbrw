import datetime as dt

from sqlalchemy import bindparam, func, lambda_stmt, or_, select
from sqlalchemy.engine import Connection

from app.tables import t_tow

select_tow = lambda_stmt(
    lambda: select(t_tow.c["kod", "kod_p", "naz", "kod_k"])
    # .where(
    #     t_tow.c.sta == "T",
    #     t_tow.c.akt == "T",
    #     t_tow.c.wsk_kuch.in_(["S", "T", "K", "X", "D"])
    # )
)


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


def get_product(conn: Connection, code: str, fir_code: str = "s13a"):
    stmt = select_tow
    stmt += lambda s: s.where(
        or_(t_tow.c.kod == bindparam("b_kod"), t_tow.c.tow_kod_pg == bindparam("b_kod"))
    )
    cen = get_product_price(conn, code.upper(), fir_code.upper())
    cen = conn.execute(
        select(func.daj_cen_br(code, cen).label("cen").label("cen"))
    ).fetchall()
    data = conn.execute(stmt, parameters={"b_kod": code.upper()}).first()

    print(data)
    return data
