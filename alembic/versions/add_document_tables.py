"""add document and paragraph tables

Revision ID: add_document_tables
Revises: add_is_pinned
Create Date: 2026-02-04

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_document_tables'
down_revision = 'add_is_pinned'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('documents',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('user_id', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('filename', sa.String(), nullable=False),
    sa.Column('file_path', sa.String(), nullable=False),
    sa.Column('file_type', sa.String(), nullable=False),
    sa.Column('file_size', sa.Integer(), nullable=False),
    sa.Column('total_paragraphs', sa.Integer(), nullable=True),
    sa.Column('total_characters', sa.Integer(), nullable=True),
    sa.Column('doc_metadata', sa.JSON(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_documents_id'), 'documents', ['id'], unique=False)
    op.create_index(op.f('ix_documents_user_id'), 'documents', ['user_id'], unique=False)
    
    op.create_table('paragraphs',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('document_id', sa.String(), nullable=False),
    sa.Column('paragraph_index', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('character_count', sa.Integer(), nullable=True),
    sa.Column('para_metadata', sa.JSON(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['document_id'], ['documents.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_paragraphs_id'), 'paragraphs', ['id'], unique=False)
    op.create_index(op.f('ix_paragraphs_document_id'), 'paragraphs', ['document_id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_paragraphs_document_id'), table_name='paragraphs')
    op.drop_index(op.f('ix_paragraphs_id'), table_name='paragraphs')
    op.drop_table('paragraphs')
    op.drop_index(op.f('ix_documents_user_id'), table_name='documents')
    op.drop_index(op.f('ix_documents_id'), table_name='documents')
    op.drop_table('documents')
