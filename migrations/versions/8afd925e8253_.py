"""empty message

Revision ID: 8afd925e8253
Revises: 
Create Date: 2025-04-01 18:45:42.984184

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8afd925e8253'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('appointment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('appointment_datetime', sa.DateTime(), nullable=False))
        batch_op.drop_column('appointment_date')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('appointment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('appointment_date', sa.DATETIME(), nullable=False))
        batch_op.drop_column('appointment_datetime')

    # ### end Alembic commands ###
