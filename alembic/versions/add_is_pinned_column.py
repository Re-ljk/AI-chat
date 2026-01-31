"""add is_pinned column

Revision ID: add_is_pinned
Revises: 3296b4e43075
Create Date: 2026-01-31

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_is_pinned'
down_revision = '3296b4e43075'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('ai_conversations', sa.Column('is_pinned', sa.Boolean(), nullable=False, server_default='false'))


def downgrade():
    op.drop_column('ai_conversations', 'is_pinned')
