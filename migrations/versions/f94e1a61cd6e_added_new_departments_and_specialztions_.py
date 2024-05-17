"""Added new departments and specialztions added and modified doctor table

Revision ID: f94e1a61cd6e
Revises: b629d0aa425b
Create Date: 2024-03-04 19:04:03.385281

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f94e1a61cd6e'
down_revision = 'b629d0aa425b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('departments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('specializations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('department_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('doctors', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'specializations', ['specialization_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('doctors', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')

    op.drop_table('specializations')
    op.drop_table('departments')
    # ### end Alembic commands ###
