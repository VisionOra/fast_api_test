"""create posts table

Revision ID: 414b48c5f647
Revises: 
Create Date: 2021-11-18 14:28:18.431567

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '414b48c5f647'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True)
    , sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
