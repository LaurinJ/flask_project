"""html_render create

Revision ID: 365061d441ac
Revises: a2b804548bf8
Create Date: 2019-11-28 18:59:05.623370

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '365061d441ac'
down_revision = 'a2b804548bf8'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("article",
                  sa.Column("html_render", sa.String, server_default=""))


def downgrade():
    op.drop_column("article", "html_rener")
