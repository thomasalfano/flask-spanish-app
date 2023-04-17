"""empty message

Revision ID: 17c4e03ba01d
Revises: 
Create Date: 2023-03-17 12:22:23.878838

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '17c4e03ba01d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    forms = op.create_table('forms',
                            sa.Column('id', sa.Integer(), nullable=False),
                            sa.Column('verb_form', sa.String(), nullable=True),
                            sa.PrimaryKeyConstraint('id'),
                            sa.UniqueConstraint('verb_form')
                            )
    op.create_table('practice_set',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('label', sa.String(length=100), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('label')
                    )
    stems = op.create_table('stems',
                            sa.Column('id', sa.Integer(), nullable=False),
                            sa.Column('stem', sa.String(length=64), nullable=True),
                            sa.PrimaryKeyConstraint('id'),
                            sa.UniqueConstraint('stem')
                            )

    pronouns = op.create_table('pronoun_number',
                               sa.Column('id', sa.Integer(), nullable=False),
                               sa.Column('number', sa.String(length=64), nullable=True),
                               sa.PrimaryKeyConstraint('id'),
                               sa.UniqueConstraint('number')
                               )

    subjects = op.create_table('subjects',
                               sa.Column('id', sa.Integer(), nullable=False),
                               sa.Column('subject', sa.String(length=64), nullable=True),
                               sa.Column('number_id', sa.Integer(), nullable=True),
                               sa.ForeignKeyConstraint(['number_id'], ['pronoun_number.id'], ),
                               sa.PrimaryKeyConstraint('id'),
                               sa.UniqueConstraint('subject')
                               )
    tenses = op.create_table('tenses',
                             sa.Column('id', sa.Integer(), nullable=False),
                             sa.Column('tense', sa.String(length=64), nullable=True),
                             sa.PrimaryKeyConstraint('id'),
                             sa.UniqueConstraint('tense')
                             )
    op.create_table('set_tenses',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('set_id', sa.Integer(), nullable=True),
                    sa.Column('tense_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['set_id'], ['practice_set.id'], ),
                    sa.ForeignKeyConstraint(['tense_id'], ['tenses.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('verbs',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('infinitive', sa.String(length=64), nullable=True),
                    sa.Column('verbForm_id', sa.Integer(), nullable=True),
                    sa.Column('stem_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['verbForm_id'], ['forms.id'], ),
                    sa.ForeignKeyConstraint(['stem_id'], ['stems.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('infinitive')
                    )
    op.create_table('irregular_conjugations',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('infin_id', sa.Integer(), nullable=True),
                    sa.Column('yo', sa.String(length=64), nullable=False),
                    sa.Column('tu', sa.String(length=64), nullable=False),
                    sa.Column('el', sa.String(length=64), nullable=False),
                    sa.Column('ella', sa.String(length=64), nullable=False),
                    sa.Column('usted', sa.String(length=64), nullable=False),
                    sa.Column('nosotros', sa.String(length=64), nullable=False),
                    sa.Column('nosotras', sa.String(length=64), nullable=False),
                    sa.Column('ellos', sa.String(length=64), nullable=False),
                    sa.Column('ellas', sa.String(length=64), nullable=False),
                    sa.Column('ustedes', sa.String(length=64), nullable=False),
                    sa.ForeignKeyConstraint(['infin_id'], ['verbs.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('set_verbs',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('set_id', sa.Integer(), nullable=True),
                    sa.Column('verb_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['set_id'], ['practice_set.id'], ),
                    sa.ForeignKeyConstraint(['verb_id'], ['verbs.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )

    # ### end Alembic commands ###
    op.bulk_insert(stems,
                   [{'id': 1, 'stem': 'o to ue'},
                    {'id': 2, 'stem': 'e to ie'},
                    {'id': 3, 'stem': 'e to i'}]
                   )

    op.bulk_insert(forms,
                   [{'id': 1, 'verb_form': 'ar verbs'},
                    {'id': 2, 'verb_form': 'er verbs'},
                    {'id': 3, 'verb_form': 'ir verbs'},
                    {'id': 4, 'verb_form': 'irregular'}]
                   )

    op.bulk_insert(tenses,
                   [{'id': 1, 'tense': 'past'},
                    {'id': 2, 'tense': 'present'},
                    {'id': 3, 'tense': 'future'}]
                   )

    op.bulk_insert(pronouns,
                   [{'id': 1, 'number': 'singular'},
                    {'id': 2, 'number': 'plural'},
                    {'id': 3, 'number': 'formal'}]
                   )

    op.bulk_insert(subjects,
                   [{'id': 1, 'subject': 'yo', 'number_id': 1},
                    {'id': 2, 'subject': 'tu', 'number_id': 1},
                    {'id': 3, 'subject': 'el', 'number_id': 1},
                    {'id': 4, 'subject': 'ella', 'number_id': 1},
                    {'id': 5, 'subject': 'usted', 'number_id': 3},
                    {'id': 6, 'subject': 'nosotros', 'number_id': 2},
                    {'id': 7, 'subject': 'nosotras', 'number_id': 2},
                    {'id': 8, 'subject': 'ellos', 'number_id': 2},
                    {'id': 9, 'subject': 'ellas', 'number_id': 2},
                    {'id': 10, 'subject': 'ustedes', 'number_id': 3}]
                   )


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('set_verbs')
    op.drop_table('irregular_conjugations')
    op.drop_table('verbs')
    op.drop_table('set_tenses')
    op.drop_table('tenses')
    op.drop_table('subjects')
    op.drop_table('stems')
    op.drop_table('practice_set')
    op.drop_table('forms')
    # ### end Alembic commands ###
