from app import db
from db_setup import Tense, Form, Subject


def pop_db():
    tenses = ['past', 'present', 'future']
    forms = ['ar verbs', 'er verbs', 'ir verbs', 'o to ue', 'e to i', 'e to ie', 'irregular']
    subjects = ['yo', 'tu', 'el/ella/usted', 'nosotros', 'vosotros', 'ellos/ellas/ustedes']
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