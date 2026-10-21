"""Initial Phase 2 schema for PostgreSQL

Revision ID: 0001_initial_phase2_schema
Revises: 
Create Date: 2026-07-23 22:15:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '0001_initial_phase2_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('full_name', sa.String(), nullable=False),
        sa.Column('role', sa.String(), nullable=False, server_default='user'),
        sa.Column('is_active', sa.Boolean(), server_default='true'),
        sa.Column('is_verified', sa.Boolean(), server_default='false'),
        sa.Column('verification_token', sa.String(), nullable=True),
        sa.Column('reset_token', sa.String(), nullable=True),
        sa.Column('refresh_token', sa.String(), nullable=True),
        sa.Column('location', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_role'), 'users', ['role'], unique=False)

    # Organizations table
    op.create_table(
        'organizations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('org_type', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('address', sa.String(), nullable=False),
        sa.Column('phone', sa.String(), nullable=False),
        sa.Column('capacity_kg_per_month', sa.Integer(), server_default='1000'),
        sa.Column('accepted_categories', sa.String(), server_default='Electronics,Plastic,Paper,Clothing,Books,Furniture,Glass,Metal,Appliances'),
        sa.Column('is_verified', sa.Boolean(), server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index(op.f('ix_organizations_id'), 'organizations', ['id'], unique=False)
    op.create_index(op.f('ix_organizations_name'), 'organizations', ['name'], unique=False)
    op.create_index(op.f('ix_organizations_org_type'), 'organizations', ['org_type'], unique=False)

    # Items table
    op.create_table(
        'items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('owner_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('category', sa.String(), nullable=False),
        sa.Column('brand', sa.String(), server_default='Generic'),
        sa.Column('image_url', sa.String(), nullable=True),
        sa.Column('age_years', sa.Float(), server_default='0.0'),
        sa.Column('usage_level', sa.String(), server_default='Moderate'),
        sa.Column('condition', sa.String(), nullable=False),
        sa.Column('original_price', sa.Float(), server_default='0.0'),
        sa.Column('estimated_price', sa.Float(), server_default='0.0'),
        sa.Column('location', sa.String(), server_default='Local City'),
        sa.Column('predicted_category', sa.String(), nullable=True),
        sa.Column('predicted_condition', sa.String(), nullable=True),
        sa.Column('recommended_action', sa.String(), server_default='Reuse'),
        sa.Column('ai_confidence', sa.Float(), server_default='0.85'),
        sa.Column('co2_saved_kg', sa.Float(), server_default='0.0'),
        sa.Column('waste_diverted_kg', sa.Float(), server_default='0.0'),
        sa.Column('environmental_impact_points', sa.Float(), server_default='0.0'),
        sa.Column('status', sa.String(), server_default='Available'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_items_category'), 'items', ['category'], unique=False)
    op.create_index(op.f('ix_items_id'), 'items', ['id'], unique=False)
    op.create_index(op.f('ix_items_owner_id'), 'items', ['owner_id'], unique=False)
    op.create_index(op.f('ix_items_recommended_action'), 'items', ['recommended_action'], unique=False)
    op.create_index(op.f('ix_items_status'), 'items', ['status'], unique=False)
    op.create_index(op.f('ix_items_title'), 'items', ['title'], unique=False)

    # Transactions table
    op.create_table(
        'transactions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('item_id', sa.Integer(), nullable=False),
        sa.Column('sender_id', sa.Integer(), nullable=False),
        sa.Column('receiver_id', sa.Integer(), nullable=True),
        sa.Column('action_type', sa.String(), nullable=False),
        sa.Column('status', sa.String(), server_default='Requested'),
        sa.Column('notes', sa.String(), nullable=True),
        sa.Column('co2_saved_kg', sa.Float(), server_default='0.0'),
        sa.Column('waste_diverted_kg', sa.Float(), server_default='0.0'),
        sa.Column('agreed_price', sa.Float(), server_default='0.0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['item_id'], ['items.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['receiver_id'], ['users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['sender_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_transactions_action_type'), 'transactions', ['action_type'], unique=False)
    op.create_index(op.f('ix_transactions_id'), 'transactions', ['id'], unique=False)
    op.create_index(op.f('ix_transactions_item_id'), 'transactions', ['item_id'], unique=False)
    op.create_index(op.f('ix_transactions_receiver_id'), 'transactions', ['receiver_id'], unique=False)
    op.create_index(op.f('ix_transactions_sender_id'), 'transactions', ['sender_id'], unique=False)
    op.create_index(op.f('ix_transactions_status'), 'transactions', ['status'], unique=False)

    # AI Logs table
    op.create_table(
        'ai_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('item_id', sa.Integer(), nullable=True),
        sa.Column('module_name', sa.String(), nullable=False),
        sa.Column('model_version', sa.String(), server_default='1.0.0'),
        sa.Column('execution_time_ms', sa.Float(), nullable=False),
        sa.Column('input_summary', sa.Text(), nullable=True),
        sa.Column('output_summary', sa.Text(), nullable=True),
        sa.Column('confidence_score', sa.Float(), nullable=True),
        sa.Column('status', sa.String(), server_default='SUCCESS'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ai_logs_id'), 'ai_logs', ['id'], unique=False)
    op.create_index(op.f('ix_ai_logs_module_name'), 'ai_logs', ['module_name'], unique=False)

    # Reports table
    op.create_table(
        'reports',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('reporter_id', sa.Integer(), nullable=False),
        sa.Column('target_item_id', sa.Integer(), nullable=True),
        sa.Column('target_user_id', sa.Integer(), nullable=True),
        sa.Column('report_type', sa.String(), server_default='system_feedback'),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('status', sa.String(), server_default='Pending'),
        sa.Column('admin_notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['reporter_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['target_item_id'], ['items.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['target_user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_reports_id'), 'reports', ['id'], unique=False)
    op.create_index(op.f('ix_reports_reporter_id'), 'reports', ['reporter_id'], unique=False)
    op.create_index(op.f('ix_reports_status'), 'reports', ['status'], unique=False)

def downgrade() -> None:
    op.drop_table('reports')
    op.drop_table('ai_logs')
    op.drop_table('transactions')
    op.drop_table('items')
    op.drop_table('organizations')
    op.drop_table('users')
