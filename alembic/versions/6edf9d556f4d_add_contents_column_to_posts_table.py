"""add contents column to posts table

Revision ID: 6edf9d556f4d
Revises: 414b48c5f647
Create Date: 2021-11-18 14:37:33.830423

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6edf9d556f4d'
down_revision = '414b48c5f647'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
