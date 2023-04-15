from . import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class IrregularConjugation(db.Model):
    """
    Database model that holds conjugations for irregular verbs.

    ForeignKey referencing the id column of Verbs
    The table contains all the possible conjugations for the irregular verb.
    """
    __tablename__ = 'irregular_conjugations'
    id = db.Column(db.Integer, primary_key=True)
    infin_id = db.Column(db.Integer, db.ForeignKey('verbs.id'))
    yo = db.Column(db.String(64), nullable=False)
    tu = db.Column(db.String(64), nullable=False)
    el = db.Column(db.String(64), nullable=False)
    ella = db.Column(db.String(64), nullable=False)
    usted = db.Column(db.String(64), nullable=False)
    nosotros = db.Column(db.String(64), nullable=False)
    nosotras = db.Column(db.String(64), nullable=False)
    ellos = db.Column(db.String(64), nullable=False)
    ellas = db.Column(db.String(64), nullable=False)
    ustedes = db.Column(db.String(64), nullable=False)


# db association table for sets and infinitives
class SetVerbs(db.Model):
    """
    Database model that represents association table between practice sets and their possible verbs.

    ForeignKey referencing the ids of practice_set and verbs tables
    """
    __tablename__ = 'set_verbs'
    id = db.Column(db.Integer, primary_key=True)
    set_id = db.Column(db.Integer, db.ForeignKey('practice_set.id'))
    verb_id = db.Column(db.Integer, db.ForeignKey('verbs.id'))

    verb = db.relationship('Verb', back_populates='practice_sets')
    practice_set = db.relationship('Practice_Set', back_populates='verbs')


# db association table for sets and verb-tenses
class SetTenses(db.Model):
    """
    Database model that represents association table between practice sets and their possible tenses.

    ForeignKey referencing the ids of practice_set and tenses tables
    """
    __tablename__ = 'set_tenses'
    id = db.Column(db.Integer, primary_key=True)
    set_id = db.Column(db.Integer, db.ForeignKey('practice_set.id'))
    tense_id = db.Column(db.Integer, db.ForeignKey('tenses.id'))

    tense = db.relationship('Tense', back_populates='practice_sets')
    practice_set = db.relationship('Practice_Set', back_populates='tenses')


class SetSubjects(db.Model):
    """
    Database model that represents the association table between the subjects table and the practice set table.

    ForeignKey referencing the ids of the practice_set and subjects table
    """
    __tablename__ = 'set_subjects'
    id = db.Column(db.Integer, primary_key=True)
    set_id = db.Column(db.Integer, db.ForeignKey('practice_set.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))

    # relationships
    subject = db.relationship('Subject', back_populates='practice_sets')
    practice_set = db.relationship('Practice_Set', back_populates='subjects')


# verb table (id, infin, verb_form(fk))
class Verb(db.Model):
    """
    Database model that contains all verbs and their respective forms

    ForeignKey - references the id of the Forms table
    Has a many-to-many relationship with SetVerbs
    """
    __tablename__ = 'verbs'
    id = db.Column(db.Integer, primary_key=True)
    infinitive = db.Column(db.String(64), unique=True)
    verbForm_id = db.Column(db.Integer, db.ForeignKey('forms.id'))
    stem_id = db.Column(db.Integer, db.ForeignKey('stems.id'), nullable=True, default=None)

    # relationship
    practice_sets = db.relationship('SetVerbs', back_populates='verb')

    def __repr__(self):
        return f"infinitive:'{self.infinitive}', 'form_id:{self.verbForm_id}'"


class Stems(db.Model):
    """
    Database model that stores the three different types of stem changers

    Has a one-to-many relationship with the Verbs table
    """

    __tablename__ = 'stems'
    id = db.Column(db.Integer, primary_key=True)
    stem = db.Column(db.String(64), unique=True)

    # relationship
    infinitives = db.relationship('Verb', backref='stem')


# verb_form [id, label] ("static")
class VerbForm(db.Model):
    """
    Database model for potential verb-forms.

    Ex.) o -> ue stem changing, or irregulars
    This table has a one-to-many relationship with the Verbs table
    """
    __tablename__ = 'forms'
    id = db.Column(db.Integer, primary_key=True)
    verb_form = db.Column(db.String, unique=True)

    # relationship
    infinitives = db.relationship('Verb', backref='verb_form')

    def __repr__(self):
        return f'{self.verb_form}'


# subject [id, label] ("static")
class Subject(db.Model):
    """ Database model for representing possible subjects to be included in question prompts. """
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(64), unique=True)
    number_id = db.Column(db.Integer, db.ForeignKey('pronoun_number.id'))

    def __repr__(self):
        return f'{self.subject}'

    # relationship
    practice_sets = db.relationship('SetSubjects', back_populates='subject')
    number = db.relationship('PronounNumber', back_populates='subjects')


class PronounNumber(db.Model):
    """Database model for the different type of pronouns, singular, plural, and formal"""
    __tablename__ = 'pronoun_number'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(64), unique=True)

    # relationship
    subjects = db.relationship('Subject', back_populates='number')


# tense [id, label]
class Tense(db.Model):
    """
    Database model for possible tenses.

    Tenses will be used in the practice-set creation process, to help lookup the correct verb_form of infinitives.
    This table has many-to-many relationship with SetTenses
    """
    __tablename__ = 'tenses'
    id = db.Column(db.Integer, primary_key=True)
    tense = db.Column(db.String(64), unique=True)

    # relationship
    practice_sets = db.relationship('SetTenses', back_populates='tense')

    def __repr__(self):
        return f'{self.tense}'


# practice_set [id, label]
class Practice_Set(db.Model):
    """
    Database model for Practice Set titles.

    Has one-to-many relationship with SetVerbs and SetTenses tables
    """
    __tablename__ = 'practice_set'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(100), unique=True)

    # relationship for table
    verbs = db.relationship('SetVerbs', back_populates='practice_set')
    tenses = db.relationship('SetTenses', back_populates='practice_set')
    subjects = db.relationship('SetSubjects', back_populates='practice_set')

    def __repr__(self):
        return f'{self.label}'


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
