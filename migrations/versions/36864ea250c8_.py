"""empty message

Revision ID: 36864ea250c8
Revises: f4bf485ca73d
Create Date: 2020-11-23 10:21:59.260767

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36864ea250c8'
down_revision = 'f4bf485ca73d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('live',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_live_name'), 'live', ['name'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_live_name'), table_name='live')
    op.drop_table('live')
    # ### end Alembic commands ###