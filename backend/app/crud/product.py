import datetime as dt

import pandas as pd
import sqlalchemy as sa
import sqlmodel as sm

from app.api.deps import OracleConnectionDep, SessionDep
from app.models import Feature, Product, ProductFeatureLink
from app.tables import t_c_slo, t_p_c_zest, t_rod_c, t_tow

select_tow = sa.lambda_stmt(
    lambda: sa.select(
        t_tow.c.kod.label("code"),
        t_tow.c.kod_p.label("index"),
        t_tow.c.naz.label("name"),
        t_tow.c.naz_p.label("full_name"),
        sa.func.meblecom.to_czy_tow_plytki(t_tow.c.kod).label("is_shallow"),
        t_tow.c.tow_kod_pg.label("parent_code"),
        t_rod_c.c.naz.label("feature_name"),
        t_c_slo.c.naz.label("feature_value"),
    )
    .join(t_p_c_zest, t_tow.c.c_zest_id == t_p_c_zest.c.c_zest_id, isouter=True)
    .join(t_rod_c, t_p_c_zest.c.c_slo_rod_c_kod == t_rod_c.c.kod, isouter=True)
    .join(
        t_c_slo,
        sa.and_(
            t_p_c_zest.c.c_slo_kod == t_c_slo.c.kod,
            t_rod_c.c.kod == t_c_slo.c.rod_c_kod,
        ),
        isouter=True,
    )
    .where(
        t_tow.c.sta == "T",
        t_tow.c.akt == "T",
        t_tow.c.wsk_kuch.in_(["S", "T", "K", "X", "D"]),
        sa.func.nvl(
            sa.func.meblecom.daj_status(t_tow.c.kod, sa.bindparam("b_date")), "A"
        )
        != "W",
        ~t_tow.c.kod_p.startswith("PROTOTYP"),
    )
)


def sync_data(
    session: SessionDep,
    conn: OracleConnectionDep,
    data,
    fir_code: str,
):
    for row in data:
        product = session.exec(
            sm.select(Product).where(Product.code == row.code)
        ).one_or_none()
        if not product:
            cen = conn.execute(
                sa.func.daj_cen_br(
                    row.code, get_product_price(conn, row.code, fir_code.upper())
                )
            ).scalar()
            print(f"dodaje {row.index}")
            product = Product.model_validate(row._mapping)
            product.price = cen
            product.parent_code = row.parent_code
            product.price_updated_at = dt.date.today()
        elif product.price_updated_at < dt.date.today():
            cen = conn.execute(
                sa.func.daj_cen_br(
                    row.code, get_product_price(conn, row.code, fir_code.upper())
                )
            ).scalar()
            print(f"aktualizuje {row.index}")
            product.price = cen
            product.price_updated_at = dt.date.today()

        feature = session.exec(
            sm.select(Feature).where(
                Feature.feature_name == row.feature_name,
                Feature.feature_value == row.feature_value,
            )
        ).one_or_none()

        produc_features_link = None
        if feature:
            produc_features_link = session.exec(
                sm.select(ProductFeatureLink).where(
                    ProductFeatureLink.product_id == product.id,
                    ProductFeatureLink.feature_id == feature.id,
                )
            ).one_or_none()

        if not produc_features_link and row.parent_code:
            if feature:
                product.features.append(feature)
            else:
                product.features.append(
                    Feature(
                        feature_name=row.feature_name,
                        feature_value=row.feature_value,
                    )
                )

        session.add(product)
        session.commit()


def get_product_price(
    conn: OracleConnectionDep, code: str, fir_code: str, kh_code: str = "000000"
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


def convert_to_nested_dict(
    data, main_group: list, nested_group_name: str, nested_group: list
):
    return (
        pd.DataFrame(data)
        .groupby(main_group)[nested_group]
        .apply(lambda x: x.to_dict("records"))
        .reset_index(name=nested_group_name)
        .to_dict("records")
    )


def get_product(
    session: SessionDep, conn: OracleConnectionDep, code: str, fir_code: str
):
    params = {"b_kod": [code.upper()], "b_date": dt.date.today()}

    local_stmt = sm.select(Product).where(Product.code.in_(sm.bindparam("b_kod")))

    remote_stmt = select_tow
    remote_stmt += lambda s: s.where(
        sa.and_(
            sa.and_(
                sa.or_(
                    t_tow.c.kod.in_(sa.bindparam("b_kod")),
                    t_tow.c.tow_kod_pg == code,
                ),
            ),
        )
    )
    remote_data = conn.execute(remote_stmt, parameters=params).all()
    if remote_data:
        sync_data(session, conn, data=remote_data, fir_code=fir_code)
    return session.exec(local_stmt, params=params).first()


def get_products_by_name(
    session: SessionDep,
    conn: OracleConnectionDep,
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
    remote_where = sa.and_(
        *[t_tow.c.naz.icontains(n.strip()) for n in name.strip().split(" ")]
    )

    remote_stmt = select_tow + (
        lambda s: s.where(remote_where).offset(offset).limit(limit + 10)
    )

    data = conn.execute(remote_stmt, parameters={"b_date": dt.date.today()}).fetchall()

    sync_data(
        session,
        conn,
        data=data,
        fir_code=fir_code,
    )

    return session.exec(local_stmt).all()
