import os
from app import create_app, db
from app.models import Subject, Tense, VerbForm, Verb, SetVerbs, SetTenses, SetSubjects, Stems, Practice_Set, \
    IrregularConjugation
from flask_migrate import Migrate

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Subject=Subject, Tense=Tense, Form=VerbForm, Verb=Verb, SetVerbs=SetVerbs, SetTenses=SetTenses,
                SetSubjects=SetSubjects, Stems=Stems, Practice_Set=Practice_Set,
                IrregularConjugation=IrregularConjugation)
