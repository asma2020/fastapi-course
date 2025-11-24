"""create votes table — FINAL VERSION THAT WORKS WITH owner_id

Revision ID: 0cd5add205ab
Revises: aa71c9c8882c
Create Date: 2025-11-23 20:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '0cd5add205ab'
down_revision = 'aa71c9c8882c'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'votes',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('post_id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('user_id', 'post_id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
    )
    # Optional: add index for faster queries
    op.create_index('ix_votes_user_post', 'votes', ['user_id', 'post_id'], unique=True)

def downgrade():
    op.drop_index('ix_votes_user_post', table_name='votes')
    op.drop_table('votes')