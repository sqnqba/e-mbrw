"""Init models

Revision ID: 10be310c6d20
Revises:
Create Date: 2024-12-12 16:33:02.482220

"""

import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from alembic import op

# revision identifiers, used by Alembic.
revision = "10be310c6d20"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "feature",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column(
            "feature_name",
            sqlmodel.sql.sqltypes.AutoString(length=64),
            nullable=False,
            unique=True,
        ),
        sa.Column(
            "feature_value",
            sqlmodel.sql.sqltypes.AutoString(length=128),
            nullable=False,
            unique=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "product",
        sa.Column("code", sqlmodel.sql.sqltypes.AutoString(length=6), nullable=False),
        sa.Column(
            "index", sqlmodel.sql.sqltypes.AutoString(length=512), nullable=False
        ),
        sa.Column(
            "name", sqlmodel.sql.sqltypes.AutoString(length=4096), nullable=False
        ),
        sa.Column(
            "full_name", sqlmodel.sql.sqltypes.AutoString(length=512), nullable=False
        ),
        sa.Column(
            "parent_code", sqlmodel.sql.sqltypes.AutoString(length=6), nullable=True
        ),
        sa.Column("is_shallow", sa.Boolean(), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("price_updated_at", sa.Date(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )
    op.create_table(
        "user",
        sa.Column(
            "ora_id", sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True
        ),
        sa.Column("email", sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_superuser", sa.Boolean(), nullable=False),
        sa.Column(
            "full_name", sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True
        ),
        sa.Column("oso_kod", sqlmodel.sql.sqltypes.AutoString(length=6), nullable=True),
        sa.Column(
            "fir_kod", sqlmodel.sql.sqltypes.AutoString(length=4), nullable=False
        ),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column(
            "hashed_password", sqlmodel.sql.sqltypes.AutoString(), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_ora_id"), "user", ["ora_id"], unique=True)
    op.create_table(
        "order",
        sa.Column(
            "fir_kod", sqlmodel.sql.sqltypes.AutoString(length=4), nullable=False
        ),
        sa.Column(
            "comment", sqlmodel.sql.sqltypes.AutoString(length=1024), nullable=True
        ),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("safo_id", sa.Integer(), nullable=True),
        sa.Column("safo_nr", sa.Integer(), nullable=True),
        sa.Column("kh_kod", sqlmodel.sql.sqltypes.AutoString(length=6), nullable=False),
        sa.Column(
            "kh_naz", sqlmodel.sql.sqltypes.AutoString(length=512), nullable=False
        ),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("owner_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(["owner_id"], ["user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_order_safo_id"), "order", ["safo_id"], unique=False)
    op.create_index(op.f("ix_order_safo_nr"), "order", ["safo_nr"], unique=False)
    op.create_table(
        "productfeaturelink",
        sa.Column("product_id", sa.Uuid(), nullable=False),
        sa.Column("feature_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["feature_id"],
            ["feature.id"],
        ),
        sa.ForeignKeyConstraint(["product_id"], ["product.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("product_id", "feature_id"),
    )
    op.create_table(
        "orderitem",
        sa.Column("quantity", sa.Float(), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("order_id", sa.Uuid(), nullable=False),
        sa.Column("product_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(["order_id"], ["order.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["product.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("orderitem")
    op.drop_table("productfeaturelink")
    op.drop_index(op.f("ix_order_safo_nr"), table_name="order")
    op.drop_index(op.f("ix_order_safo_id"), table_name="order")
    op.drop_table("order")
    op.drop_index(op.f("ix_user_ora_id"), table_name="user")
    op.drop_table("user")
    op.drop_table("product")
    op.drop_table("feature")
    # ### end Alembic commands ###
