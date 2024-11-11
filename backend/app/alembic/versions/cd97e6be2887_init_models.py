"""Init models

Revision ID: cd97e6be2887
Revises:
Create Date: 2024-11-09 22:13:19.678872

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = 'cd97e6be2887'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('ora_id', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True),
    sa.Column('email', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('full_name', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True),
    sa.Column('oso_kod', sqlmodel.sql.sqltypes.AutoString(length=6), nullable=True),
    sa.Column('fir_kod', sqlmodel.sql.sqltypes.AutoString(length=4), nullable=True),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('hashed_password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=False)
    op.create_index(op.f('ix_user_ora_id'), 'user', ['ora_id'], unique=True)
    op.create_table('order',
    sa.Column('safo_nr', sa.Integer(), nullable=True),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('safo_id', sa.Integer(), nullable=True),
    sa.Column('kh_kod', sqlmodel.sql.sqltypes.AutoString(length=6), nullable=False),
    sa.Column('fir_kod', sqlmodel.sql.sqltypes.AutoString(length=4), nullable=True),
    sa.Column('owner_id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_order_safo_id'), 'order', ['safo_id'], unique=False)
    op.create_index(op.f('ix_order_safo_nr'), 'order', ['safo_nr'], unique=False)
    op.create_table('orderitem',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('order_id', sa.Uuid(), nullable=False),
    sa.Column('product_id', sa.Uuid(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('orderitem')
    op.drop_index(op.f('ix_order_safo_nr'), table_name='order')
    op.drop_index(op.f('ix_order_safo_id'), table_name='order')
    op.drop_table('order')
    op.drop_index(op.f('ix_user_ora_id'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('product')
    # ### end Alembic commands ###
