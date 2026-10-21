"""Add inventory fields to items table

Revision ID: 0002_add_inventory_fields_to_item
Revises: 0001_initial_phase2_schema
Create Date: 2026-07-23 23:30:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '0002_add_inventory_fields_to_item'
down_revision: Union[str, None] = '0001_initial_phase2_schema'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.add_column('items', sa.Column('organization_id', sa.Integer(), nullable=True))
    op.add_column('items', sa.Column('item_name', sa.String(), nullable=True))
    op.add_column('items', sa.Column('quantity', sa.Integer(), server_default='1', nullable=False))
    op.add_column('items', sa.Column('unit', sa.String(), server_default='pcs', nullable=False))
    op.add_column('items', sa.Column('price', sa.Float(), server_default='0.0', nullable=False))
    
    op.create_index(op.f('ix_items_organization_id'), 'items', ['organization_id'], unique=False)
    op.create_index(op.f('ix_items_item_name'), 'items', ['item_name'], unique=False)
    op.create_index(op.f('ix_items_quantity'), 'items', ['quantity'], unique=False)
    op.create_index(op.f('ix_items_price'), 'items', ['price'], unique=False)
    
    op.create_foreign_key('fk_items_organization_id', 'items', 'organizations', ['organization_id'], ['id'], ondelete='SET NULL')

def downgrade() -> None:
    op.drop_constraint('fk_items_organization_id', 'items', type_='foreignkey')
    op.drop_index(op.f('ix_items_price'), table_name='items')
    op.drop_index(op.f('ix_items_quantity'), table_name='items')
    op.drop_index(op.f('ix_items_item_name'), table_name='items')
    op.drop_index(op.f('ix_items_organization_id'), table_name='items')
    
    op.drop_column('items', 'price')
    op.drop_column('items', 'unit')
    op.drop_column('items', 'quantity')
    op.drop_column('items', 'item_name')
    op.drop_column('items', 'organization_id')
