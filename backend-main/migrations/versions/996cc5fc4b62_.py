"""empty message

Revision ID: 996cc5fc4b62
Revises: 
Create Date: 2023-07-14 18:53:37.003357

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '996cc5fc4b62'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Text(), nullable=False),
    sa.Column('customer_id', sa.Text(), nullable=True),
    sa.Column('type', sa.String(length=100), nullable=True),
    sa.Column('email', sa.Text(), nullable=False),
    sa.Column('phone', sa.Text(), nullable=True),
    sa.Column('address', sa.Text(), nullable=True),
    sa.Column('company_type', sa.Text(), nullable=True),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('password', sa.Text(), nullable=True),
    sa.Column('company', sa.Text(), nullable=True),
    sa.Column('credit', sa.Text(), nullable=True),
    sa.Column('subscription_credit', sa.Text(), nullable=True),
    sa.Column('email_verified', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('last_login', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('customer_id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('analyse',
    sa.Column('id', sa.Text(), nullable=False),
    sa.Column('filename', sa.Text(), nullable=True),
    sa.Column('file_byte', sa.LargeBinary(), nullable=True),
    sa.Column('analyzed', sa.Boolean(), nullable=True),
    sa.Column('analyse_data', sa.JSON(), nullable=True),
    sa.Column('budget', sa.Float(), nullable=True),
    sa.Column('created_by', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('verification',
    sa.Column('id', sa.Text(), nullable=False),
    sa.Column('type', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Text(), nullable=True),
    sa.Column('note', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('verification')
    op.drop_table('analyse')
    op.drop_table('user')
    # ### end Alembic commands ###
