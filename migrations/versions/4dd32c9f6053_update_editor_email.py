"""update editor email

Revision ID: 4dd32c9f6053
Revises: 3a4946dca69c
Create Date: 2016-01-07 12:39:39.130160

"""

# revision identifiers, used by Alembic.
revision = '4dd32c9f6053'
down_revision = '3a4946dca69c'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute("UPDATE contributor SET email = 'harald.hammarstrom@gmail.com'")


def downgrade():
    pass
