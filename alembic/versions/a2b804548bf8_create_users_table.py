"""Create users table

Revision ID: a2b804548bf8
Revises: 
Create Date: 2019-11-14 19:36:09.500226

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2b804548bf8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.String, unique=True),
        sa.Column("password", sa.String)
    )


def downgrade():
    op.drop_table("user")
