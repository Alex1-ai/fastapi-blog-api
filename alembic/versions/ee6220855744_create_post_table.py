"""create post table

Revision ID: ee6220855744
Revises: 714025a400d3
Create Date: 2026-10-06 18:26:04.515522

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ee6220855744'
down_revision: Union[str, Sequence[str], None] = '714025a400d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'posts',
        sa.Column(
            'id',
            sa.Integer(),
            nullable=False,
            primary_key=True
        ),
        sa.Column(
            'title',
            sa.String(),
            nullable=False
        ),
        sa.Column(
            'content',
            sa.String(),
            nullable=False
        ),
        sa.Column(
            'published',
            sa.Boolean(),
            nullable=False,
            server_default='TRUE'
        ),
        sa.Column(
            'rating',
            sa.Numeric(2, 1),
            nullable=True,
            server_default='0.0'
        ),
        sa.Column(
            'created_at',
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text('now()')
        )
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('posts')

