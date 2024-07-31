"""Add a column

Revision ID: a4697a896021
Revises: dd879cb7e7f1
Create Date: 2024-07-30 11:44:23.412548

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a4697a896021'
down_revision: Union[str, None] = 'dd879cb7e7f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
