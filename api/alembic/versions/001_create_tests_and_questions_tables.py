"""Create tests and questions tables

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create tests table
    op.create_table('tests',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('slug', sa.String(length=100), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tests_id'), 'tests', ['id'], unique=False)
    op.create_index(op.f('ix_tests_slug'), 'tests', ['slug'], unique=False)
    op.create_index('idx_tests_slug', 'tests', ['slug'], unique=False)
    op.create_index('idx_tests_active', 'tests', ['is_active'], unique=False)
    op.create_unique_constraint('uq_tests_slug', 'tests', ['slug'])

    # Create questions table
    op.create_table('questions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('test_id', sa.Integer(), nullable=False),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('order', sa.Integer(), nullable=False),
        sa.Column('type', sa.String(length=50), nullable=False),
        sa.Column('config', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['test_id'], ['tests.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_questions_id'), 'questions', ['id'], unique=False)
    op.create_index(op.f('ix_questions_test_id'), 'questions', ['test_id'], unique=False)
    op.create_index('idx_questions_test_id', 'questions', ['test_id'], unique=False)
    op.create_index('idx_questions_test_order', 'questions', ['test_id', 'order'], unique=False)


def downgrade() -> None:
    # Drop questions table first (due to foreign key constraint)
    op.drop_index('idx_questions_test_order', table_name='questions')
    op.drop_index('idx_questions_test_id', table_name='questions')
    op.drop_index(op.f('ix_questions_test_id'), table_name='questions')
    op.drop_index(op.f('ix_questions_id'), table_name='questions')
    op.drop_table('questions')

    # Drop tests table
    op.drop_index('idx_tests_active', table_name='tests')
    op.drop_index('idx_tests_slug', table_name='tests')
    op.drop_index(op.f('ix_tests_slug'), table_name='tests')
    op.drop_index(op.f('ix_tests_id'), table_name='tests')
    op.drop_constraint('uq_tests_slug', 'tests', type_='unique')
    op.drop_table('tests')

