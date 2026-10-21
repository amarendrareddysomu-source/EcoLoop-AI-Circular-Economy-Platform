"""Add transaction fields to transactions table

Revision ID: 0003_add_transaction_fields
Revises: 0002_add_inventory_fields_to_item
Create Date: 2026-07-23 23:45:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '0003_add_transaction_fields'
down_revision: Union[str, None] = '0002_add_inventory_fields_to_item'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.add_column('transactions', sa.Column('transaction_type', sa.String(), nullable=True))
    op.add_column('transactions', sa.Column('seller_id', sa.Integer(), nullable=True))
    op.add_column('transactions', sa.Column('buyer_id', sa.Integer(), nullable=True))
    op.add_column('transactions', sa.Column('organization_id', sa.Integer(), nullable=True))
    op.add_column('transactions', sa.Column('quantity', sa.Integer(), server_default='1', nullable=False))
    op.add_column('transactions', sa.Column('unit_price', sa.Float(), server_default='0.0', nullable=False))
    op.add_column('transactions', sa.Column('total_amount', sa.Float(), server_default='0.0', nullable=False))
    op.add_column('transactions', sa.Column('transaction_status', sa.String(), server_default='Pending', nullable=False))
    op.add_column('transactions', sa.Column('payment_status', sa.String(), server_default='Unpaid', nullable=False))

    # Alter sender_id to nullable=True for flexibility
    with op.batch_alter_table('transactions') as batch_op:
        batch_op.alter_column('sender_id', existing_type=sa.Integer(), nullable=True)
        batch_op.alter_column('action_type', existing_type=sa.String(), nullable=True)

    op.create_index(op.f('ix_transactions_transaction_type'), 'transactions', ['transaction_type'], unique=False)
    op.create_index(op.f('ix_transactions_seller_id'), 'transactions', ['seller_id'], unique=False)
    op.create_index(op.f('ix_transactions_buyer_id'), 'transactions', ['buyer_id'], unique=False)
    op.create_index(op.f('ix_transactions_organization_id'), 'transactions', ['organization_id'], unique=False)
    op.create_index(op.f('ix_transactions_quantity'), 'transactions', ['quantity'], unique=False)
    op.create_index(op.f('ix_transactions_unit_price'), 'transactions', ['unit_price'], unique=False)
    op.create_index(op.f('ix_transactions_total_amount'), 'transactions', ['total_amount'], unique=False)
    op.create_index(op.f('ix_transactions_transaction_status'), 'transactions', ['transaction_status'], unique=False)
    op.create_index(op.f('ix_transactions_payment_status'), 'transactions', ['payment_status'], unique=False)

    op.create_foreign_key('fk_transactions_seller_id', 'transactions', 'users', ['seller_id'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('fk_transactions_buyer_id', 'transactions', 'users', ['buyer_id'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('fk_transactions_organization_id', 'transactions', 'organizations', ['organization_id'], ['id'], ondelete='SET NULL')

def downgrade() -> None:
    op.drop_constraint('fk_transactions_organization_id', 'transactions', type_='foreignkey')
    op.drop_constraint('fk_transactions_buyer_id', 'transactions', type_='foreignkey')
    op.drop_constraint('fk_transactions_seller_id', 'transactions', type_='foreignkey')

    op.drop_index(op.f('ix_transactions_payment_status'), table_name='transactions')
    op.drop_index(op.f('ix_transactions_transaction_status'), table_name='transactions')
    op.drop_index(op.f('ix_transactions_total_amount'), table_name='transactions')
    op.drop_index(op.f('ix_transactions_unit_price'), table_name='transactions')
    op.drop_index(op.f('ix_transactions_quantity'), table_name='transactions')
    op.drop_index(op.f('ix_transactions_organization_id'), table_name='transactions')
    op.drop_index(op.f('ix_transactions_buyer_id'), table_name='transactions')
    op.drop_index(op.f('ix_transactions_seller_id'), table_name='transactions')
    op.drop_index(op.f('ix_transactions_transaction_type'), table_name='transactions')

    op.drop_column('transactions', 'payment_status')
    op.drop_column('transactions', 'transaction_status')
    op.drop_column('transactions', 'total_amount')
    op.drop_column('transactions', 'unit_price')
    op.drop_column('transactions', 'quantity')
    op.drop_column('transactions', 'organization_id')
    op.drop_column('transactions', 'buyer_id')
    op.drop_column('transactions', 'seller_id')
    op.drop_column('transactions', 'transaction_type')
