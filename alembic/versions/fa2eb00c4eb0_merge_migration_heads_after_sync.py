"""merge migration heads after sync

Revision ID: fa2eb00c4eb0
Revises: 635034d0c398, 799e68fe3a15
Create Date: 2026-02-12 13:31:09.915675

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fa2eb00c4eb0'
down_revision: Union[str, Sequence[str], None] = ('635034d0c398', '799e68fe3a15')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
