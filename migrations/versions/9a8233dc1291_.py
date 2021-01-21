"""empty message

Revision ID: 9a8233dc1291
Revises: 65ad32d5ea4b
Create Date: 2021-01-20 05:19:11.798524

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a8233dc1291'
down_revision = '65ad32d5ea4b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('medico', 'cambio',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('medico', 'verificaion',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('medico', 'verificaion',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.alter_column('medico', 'cambio',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    # ### end Alembic commands ###