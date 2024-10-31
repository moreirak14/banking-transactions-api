"""create bank accounts table

Revision ID: a2a2e2f19fc7
Revises:
Create Date: 2024-10-31 17:03:07.795510

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a2a2e2f19fc7"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create the sequence
    op.execute(sa.text("CREATE SEQUENCE account_number_seq START 1"))

    # Create the table
    op.create_table(
        "bank_accounts",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column(
            "account_number",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("nextval('account_number_seq')"),
        ),
        sa.Column("balance", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("account_number"),
        sa.UniqueConstraint("id"),
    )


def downgrade() -> None:
    # Drop the table
    op.drop_table("bank_accounts")

    # Drop the sequence
    op.execute(sa.text("DROP SEQUENCE account_number_seq"))
