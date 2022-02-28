"""add user table

Revision ID: 31365528fd38
Revises: 6edf9d556f4d
Create Date: 2021-11-18 14:48:33.198900

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31365528fd38'
down_revision = '6edf9d556f4d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')

    pass
