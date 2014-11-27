"""fix polymorphic_type

Revision ID: 2e4cd688cfee
Revises: 
Create Date: 2014-11-26 15:29:45.439000

"""

# revision identifiers, used by Alembic.
revision = '2e4cd688cfee'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    update_pmtype(['language', 'value', 'contribution', 'parameter'], 'base', 'custom')


def downgrade():
    update_pmtype(['language', 'value', 'contribution', 'parameter'], 'custom', 'base')


def update_pmtype(tablenames, before, after):
    for table in tablenames:
        op.execute(sa.text('UPDATE %s SET polymorphic_type = :after '
            'WHERE polymorphic_type = :before' % table
            ).bindparams(before=before, after=after))
