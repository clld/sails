"""update contact email

Revision ID: 3a4946dca69c
Revises: 2e4cd688cfee
Create Date: 2016-01-07 12:29:33.259596

"""

# revision identifiers, used by Alembic.
revision = '3a4946dca69c'
down_revision = '2e4cd688cfee'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute("UPDATE dataset SET contact = 'harald.hammarstrom@gmail.com'")


def downgrade():
    pass
