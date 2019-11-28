"""add newsletter

Revision ID: 1d4ea7d00c64
Revises: 365061d441ac
Create Date: 2019-11-28 20:28:08.835565

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1d4ea7d00c64'
down_revision = '365061d441ac'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "newsletter",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", sa.String, unique=True)
    )


def downgrade():
    op.drop_table("newsletter")
