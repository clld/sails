"""update license image

Revision ID: d8058a6ab145
Revises: 28a68c79eefd
Create Date: 2018-08-14 14:44:11.949671

"""

# revision identifiers, used by Alembic.
revision = 'd8058a6ab145'
down_revision = '28a68c79eefd'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute("""UPDATE dataset SET jsondata = '{"license_name": "Creative Commons Attribution-NonCommercial-NoDerivs 2.0 Germany", "license_icon": "cc-by-nc-nd.png"}'""")


def downgrade():
    pass
