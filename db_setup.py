from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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


# verb table (id, infin, form(fk))
class Verb(db.Model):
    """
    Database model that contains all verbs and their respective forms

    ForeignKey - references the id of the Forms table
    Has a many-to-many relationship with SetVerbs
    """
    __tablename__ = 'verbs'
    id = db.Column(db.Integer, primary_key=True)
    infinitive = db.Column(db.String(64), unique=True)
    form_id = db.Column(db.Integer, db.ForeignKey('forms.id'))
    stem_id = db.Column(db.Integer, db.ForeignKey('stems.id'), nullable=True, default=None)

    # relationship
    practice_sets = db.relationship('SetVerbs', back_populates='verb')

    def __repr__(self):
        return f"infinitive:'{self.infinitive}', 'form_id:{self.form_id}'"


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


# form [id, label] ("static")
class Form(db.Model):
    """
    Database model for potential verb-forms.

    Ex.) o -> ue stem changing, or irregulars
    This table has a one-to-many relationship with the Verbs table
    """
    __tablename__ = 'forms'
    id = db.Column(db.Integer, primary_key=True)
    form = db.Column(db.String, unique=True)

    # relationship
    infinitives = db.relationship('Verb', backref='form')

    def __repr__(self):
        return f'{self.form}'


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

    Tenses will be used in the practice-set creation process, to help lookup the correct form of infinitives.
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


def insert():
    """ Populates database's static tables with data."""
    tenses = ['past', 'present', 'future']
    forms = ['ar verbs', 'er verbs', 'ir verbs', 'o to ue', 'e to i', 'e to ie', 'irregular']
    subjects = ['yo', 'tu', 'el', 'ella', 'usted', 'nosotros', 'vosotros', 'ellos', 'ellas', 'ustedes']

    for i in tenses:
        db.session.add(Tense(tense=i))
        db.session.commit()

    for i in forms:
        db.session.add(Form(form=i))
        db.session.commit()

    for i in subjects:
        db.session.add(Subject(subject=i))
        db.session.commit()
    print('DB Populated successfully!')


if __name__ == '__main__':
    pass
