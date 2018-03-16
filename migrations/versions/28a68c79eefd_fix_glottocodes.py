"""fix glottocodes

Revision ID: 28a68c79eefd
Revises: 2ab08f83f725
Create Date: 2018-03-16 09:32:45.554505

"""
import re

# revision identifiers, used by Alembic.
revision = '28a68c79eefd'
down_revision = '2ab08f83f725'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    conn = op.get_bind()
    glottocodes = list(
        conn.execute("select pk, name from identifier where type = 'glottolog'"))
    for pk, gc in glottocodes:
        gc = gc.replace('{', '').replace('}', '')
        assert re.match('[a-z]{4}[0-9]{4}$', gc)
        conn.execute("update identifier set name = %s where pk = %s", (gc, pk))


def downgrade():
    pass
