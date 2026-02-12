"""limiting email size in users table

Revision ID: 94f815895f47
Revises: 0c90a5132b7d
Create Date: 2026-02-12 13:41:31.975168

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '94f815895f47'
down_revision: Union[str, Sequence[str], None] = '0c90a5132b7d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None: 
    op.alter_column('users', 'email', type_=sa.String(128), existing_type=sa.String(), existing_nullable=False) 
def downgrade() -> None: 
    op.alter_column('users', 'email', type_=sa.String(), existing_type=sa.String(128), existing_nullable=False)
