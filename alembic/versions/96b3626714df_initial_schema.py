"""initial schema

Revision ID: 96b3626714df
Revises: 
Create Date: 2026-06-16 17:42:16.177824

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '96b3626714df'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    DO $$ BEGIN
        CREATE TYPE partcondition AS ENUM ('NEW', 'USED_GOOD', 'USED_FAIR', 'FOR_PARTS');
    EXCEPTION
        WHEN duplicate_object THEN null;
    END $$;
    """)
    op.alter_column('part', 'condition',
               existing_type=sa.VARCHAR(),
               type_=sa.Enum('NEW', 'USED_GOOD', 'USED_FAIR', 'FOR_PARTS', name='partcondition'),
               existing_nullable=False,
               postgresql_using="condition::partcondition")
    # ### end Alembic commands ###


def downgrade() -> None:
    op.alter_column('part', 'condition',
               existing_type=sa.Enum('NEW', 'USED_GOOD', 'USED_FAIR', 'FOR_PARTS', name='partcondition'),
               type_=sa.VARCHAR(),
               existing_nullable=False,
               postgresql_using="condition::varchar")
    op.execute("DROP TYPE partcondition")
    # ### end Alembic commands ###
