"""Apply string length limits to User table

Revision ID: 799e68fe3a15
Revises: bcdfcf9efcc8
Create Date: 2026-02-12 13:10:53.525546

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '799e68fe3a15'
down_revision: Union[str, Sequence[str], None] = 'bcdfcf9efcc8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Manual instructions to change the column types
    op.alter_column('users', 'phone_number', type_=sa.String(15), existing_type=sa.String(), existing_nullable=False)
    op.alter_column('users', 'first_name', type_=sa.String(32), existing_type=sa.String(), existing_nullable=False)
    op.alter_column('users', 'last_name', type_=sa.String(32), existing_type=sa.String(), existing_nullable=True)
    op.alter_column('users', 'about', type_=sa.String(128), existing_type=sa.String(), existing_nullable=True)

def downgrade() -> None:
    # Instructions to revert the changes (make them unlimited again)
    op.alter_column('users', 'phone_number', type_=sa.String(), existing_type=sa.String(15), existing_nullable=False)
    op.alter_column('users', 'first_name', type_=sa.String(), existing_type=sa.String(32), existing_nullable=False)
    op.alter_column('users', 'last_name', type_=sa.String(), existing_type=sa.String(32), existing_nullable=True)
    op.alter_column('users', 'about', type_=sa.String(), existing_type=sa.String(128), existing_nullable=True)
