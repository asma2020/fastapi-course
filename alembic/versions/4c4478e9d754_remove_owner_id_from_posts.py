"""remove owner_id from posts

Revision ID: 4c4478e9d754
Revises: ec2d543e8057
Create Date: 2025-11-23 18:21:11.808887

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c4478e9d754'
down_revision = 'ec2d543e8057'
branch_labels = None
depends_on = None


def upgrade():
    # THIS IS ALL YOU NEED — PostgreSQL drops the FK automatically!
    op.drop_column('posts', 'owner_id')


def downgrade():
    # Recreate the column + foreign key
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        'fk_posts_owner_id_users',    # give it a name this time
        'posts', 'users',
        ['owner_id'], ['id'],
        ondelete='CASCADE'
    )