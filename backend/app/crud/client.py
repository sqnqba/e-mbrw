from sqlalchemy import and_, bindparam, func, lambda_stmt, or_, select
from sqlalchemy.engine import Connection

from app.tables import t_kh, t_kh_fir

kh_fir_exists = (
    select(t_kh_fir.c.kh_kod)
    .where(
        t_kh_fir.c.kh_kod == t_kh.c.kod,
        t_kh_fir.c.fir_kod == bindparam("b_fir_kod"),
        t_kh_fir.c.sta_od.in_(["O", "X"]),
    )
    .exists()
)

select_kh_stmt = lambda_stmt(
    lambda: select(
        t_kh.c[
            "kod",
            "naz_s",
            "naz",
            "adr_m",
            "adr_u",
            "adr_d",
        ],
        func.REGEXP_REPLACE(
            t_kh.c.adr_k, "([[:digit:]]{2})([[:digit:]].+)", "\\1-\\2"
        ).label("adr_k"),
        func.nvl(func.replace(t_kh.c.nip, "-", ""), "").label("nip"),
    )
    .where(
        and_(t_kh.c.akt == "T", kh_fir_exists),
    )
    .order_by(t_kh.c.kod)
)


def get_client(
    *,
    conn: Connection,
    code: str,
    fir_code: str | None,
):
    stmt = select_kh_stmt

    stmt += lambda s: s.where(or_(t_kh.c.kod == code))

    return conn.execute(stmt, parameters={"b_fir_kod": fir_code}).fetchone()


def get_client_by_name_nip(
    *,
    conn: Connection,
    name: str | None,
    nip: str | None,
    fir_code: str | None,
):
    stmt = select_kh_stmt

    if name:
        name = name.strip()
        where_naz = or_(
            and_(
                *[t_kh.c.naz.icontains(n.strip()) for n in name.split(" ")],
            ),
        )
        stmt += lambda s: s.where(where_naz)

    if nip:
        nip = nip.replace("-", "").strip()
        stmt += lambda s: s.where(t_kh.c.nip.startswith(nip))

    stmt += lambda s: s.limit(25)

    return conn.execute(stmt, parameters={"b_fir_kod": fir_code}).fetchall()
