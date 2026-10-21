"""Create generated_reports table

Revision ID: 0004_create_generated_reports_table
Revises: 0003_add_transaction_fields
Create Date: 2026-07-23 23:59:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '0004_create_generated_reports_table'
down_revision: Union[str, None] = '0003_add_transaction_fields'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        'generated_reports',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('report_type', sa.String(), nullable=False),
        sa.Column('period', sa.String(), nullable=False),
        sa.Column('data_json', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_generated_reports_id'), 'generated_reports', ['id'], unique=False)
    op.create_index(op.f('ix_generated_reports_user_id'), 'generated_reports', ['user_id'], unique=False)
    op.create_index(op.f('ix_generated_reports_title'), 'generated_reports', ['title'], unique=False)
    op.create_index(op.f('ix_generated_reports_report_type'), 'generated_reports', ['report_type'], unique=False)
    op.create_index(op.f('ix_generated_reports_period'), 'generated_reports', ['period'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_generated_reports_period'), table_name='generated_reports')
    op.drop_index(op.f('ix_generated_reports_report_type'), table_name='generated_reports')
    op.drop_index(op.f('ix_generated_reports_title'), table_name='generated_reports')
    op.drop_index(op.f('ix_generated_reports_user_id'), table_name='generated_reports')
    op.drop_index(op.f('ix_generated_reports_id'), table_name='generated_reports')
    op.drop_table('generated_reports')
