"""initial again

Revision ID: 1831fc5afe1e
Revises: 
Create Date: 2022-04-05 16:59:00.732199

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1831fc5afe1e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contest',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('start_date_time', sa.DateTime(), nullable=False),
    sa.Column('end_date_time', sa.DateTime(), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_contest'))
    )
    op.create_table('language',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_language'))
    )
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_role'))
    )
    op.create_table('team',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_team'))
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('first_name', sa.String(length=30), nullable=False),
    sa.Column('last_name', sa.String(length=30), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('image_file', sa.String(length=20), nullable=False),
    sa.Column('password', sa.String(length=60), nullable=False),
    sa.Column('role', sa.Integer(), nullable=False),
    sa.Column('team', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role'], ['role.id'], name=op.f('fk_user_role_role')),
    sa.ForeignKeyConstraint(['team'], ['team.id'], name=op.f('fk_user_team_team')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user')),
    sa.UniqueConstraint('email', name=op.f('uq_user_email')),
    sa.UniqueConstraint('username', name=op.f('uq_user_username'))
    )
    op.create_table('challenge',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('support_zip_file', sa.LargeBinary(), nullable=True),
    sa.Column('code_scoring', sa.LargeBinary(), nullable=True),
    sa.Column('dockerfile', sa.LargeBinary(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_challenge_user_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_challenge'))
    )
    op.create_table('contest_challenges',
    sa.Column('contest_id', sa.Integer(), nullable=True),
    sa.Column('challenge_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['challenge_id'], ['challenge.id'], name=op.f('fk_contest_challenges_challenge_id_challenge')),
    sa.ForeignKeyConstraint(['contest_id'], ['contest.id'], name=op.f('fk_contest_challenges_contest_id_contest'))
    )
    op.create_table('submission',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('time_submitted', sa.DateTime(), nullable=False),
    sa.Column('code_file', sa.LargeBinary(), nullable=True),
    sa.Column('code_output', sa.LargeBinary(), nullable=True),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('contest_id', sa.Integer(), nullable=False),
    sa.Column('challenge_id', sa.Integer(), nullable=False),
    sa.Column('language_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['challenge_id'], ['challenge.id'], name=op.f('fk_submission_challenge_id_challenge')),
    sa.ForeignKeyConstraint(['contest_id'], ['contest.id'], name=op.f('fk_submission_contest_id_contest')),
    sa.ForeignKeyConstraint(['language_id'], ['language.id'], name=op.f('fk_submission_language_id_language')),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_submission_user_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_submission'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('submission')
    op.drop_table('contest_challenges')
    op.drop_table('challenge')
    op.drop_table('user')
    op.drop_table('team')
    op.drop_table('role')
    op.drop_table('language')
    op.drop_table('contest')
    # ### end Alembic commands ###
