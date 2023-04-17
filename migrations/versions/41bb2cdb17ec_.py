"""empty message

Revision ID: 41bb2cdb17ec
Revises: 480f2b0ff7bd
Create Date: 2023-04-11 19:25:44.911769

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '41bb2cdb17ec'
down_revision = '480f2b0ff7bd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    users = op.create_table('users',
                            sa.Column('id', sa.Integer(), nullable=False),
                            sa.Column('username', sa.String(length=64), nullable=True),
                            sa.Column('password_hash', sa.String(length=128), nullable=True),
                            sa.PrimaryKeyConstraint('id')
                            )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_users_username'), ['username'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_users_username'))

    op.drop_table('users')
    # ### end Alembic commands ###
