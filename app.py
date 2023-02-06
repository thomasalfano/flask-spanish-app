from flask import Flask, render_template, redirect, url_for, request, session, flash
import random
from db_setup import db, Verb, SetVerbs,SetTenses, Form, Subject, Practice_Set, Tense
from conjugate import conjugate_ar, conjugate_ir, conjugate_er
from forms import InfinitiveForm, CreateSetForm
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres::@localhost/flask_spanish'

# initialize db with app instance
db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


# verb view function that shows a list of all infinitives
# add infinitive to list upon form completion
@app.route('/verb-view', methods=['POST', 'GET'])
def verb_view():
    form = InfinitiveForm()
    infinitives_list = Verb.query.all()
    verb_forms = Form.query.all()
    form.form.choices = verb_forms

    # if form validates, query the verb table using form data
    # add new entry if verb does not exist
    if form.validate_on_submit():
        existing_verb = Verb.query.filter_by(infinitive=form.infinitive.data).first()

        # if not an existing verb in db
        # add new verb to db using form data
        if not existing_verb:
            form_infin = form.infinitive.data
            verb_form = db.session.query(Form).filter_by(form=form.form.data).first()
            new_verb = Verb(infinitive=form_infin, form=verb_form)
            db.session.add(new_verb)
            db.session.commit()

            # clear form data after successful entry
            form.infinitive.data = ''
            form.form.data = ''
            # query all verbs so that new addition shows in HTML rendering
            infinitives_list = Verb.query.all()

            return render_template('verb_view.html', infinitives_list=infinitives_list, form=form)
        else:
            flash('This infinitive exists already', category='message')
            return render_template('verb_view.html', infinitives_list=infinitives_list, form=form)
    else:
        return render_template('verb_view.html', infinitives_list=infinitives_list, form=form)


# setup route for creating 'practice sets'
@app.route('/setup', methods=['GET', 'POST'])
def setup():
    form = CreateSetForm()
    tense_choices = Tense.query.all()
    infinitives_list = Verb.query.all()
    form.tenses.choices = [str(i) for i in tense_choices]
    form.infinitives.choices = [i.infinitive for i in infinitives_list]

    if form.validate_on_submit():

        set_title = form.title.data
        tenses = form.tenses.data
        infinitives = form.infinitives.data

        # clear form entry
        form.title.data = ''
        form.tenses.data = ''
        form.infinitives.data = ''

        # add new practice set title to db if not found in query
        existing_set = Practice_Set.query.filter_by(label=form.title.data).first()
        if not existing_set:
            new_set = Practice_Set(label=set_title)
            db.session.add(new_set)
            db.session.commit()

            # query the addition that was just made
            query_set = db.session.query(Practice_Set).filter_by(label=set_title).first()

            # for infinitives selected in form, add to set_verbs
            # EX:
            #    set_id    verb_id
            #       1          2
            #       1          3
            for infin in infinitives:
                # query the infinitive
                query_infin = Verb.query.filter_by(infinitive=infin).first()

                set_infin = SetVerbs(verb=query_infin, practice_set=query_set)
                db.session.add(set_infin)

            # repeat above step for tenses
            for i in tenses:
                # query the tense
                query_tense = Tense.query.filter_by(tense=i).first()
                
                set_tense = SetTenses(tense=query_tense, practice_set=query_set)
                db.session.add(set_tense)
            db.session.commit()
            return redirect(url_for('practice_select'))
        else:
            return 'something went wrong'

    else:
        return render_template('setup.html', form=form)


# route for selecting which 'practice set' to be used
@app.route('/practice-select', methods=['GET', 'POST'])
def practice_select():
    practice_sets = Practice_Set.query.all()
    return render_template('practice_select.html', practice_sets=practice_sets)


# student facing practice screen that uses conjugation function to check student answers for correctness
@app.route('/practice/<active_set>', methods=['GET', 'POST'])
def practice(active_set):
    session['set'] = active_set
    query_set = db.session.query(Practice_Set).filter_by(label=active_set).first()
    available_infinitives = db.session.query(Verb).all()
    available_tenses = db.session.query(Tense).all()
    session['correct'] = False
    session['incorrect'] = False
    subjects = Subject.query.all()

    if request.method == 'POST':
        session['user_answer'] = request.form.get('answer')

        if session.get('user_answer') == session.get('correct_answer'):
            session['correct'] = True
            session['incorrect'] = False
        else:
            session['correct'] = False
            session['incorrect'] = True

        return render_template('practice_view.html', title=active_set,
                               correct_answer=session.get('correct_answer'),
                               infinitive=session.get('infinitive'),
                               subject=session.get('subj'),
                               tense=session.get('tense'),
                               correct=session.get('correct'),
                               incorrect=session.get('incorrect'))

    else:
        # randomly select from infin, subj, and tense lists
        # to be used in view function for prompt
        rand_infin = random.choice(available_infinitives)
        rand_subj = random.choice(subjects)
        rand_tense = random.choice(available_tenses)

        session['infinitive'] = rand_infin.infinitive
        session['subj'] = rand_subj.subject
        session['tense'] = rand_tense.tense
        infinitive = session.get('infinitive')
        subj = session.get('subj')
        tense = session.get('tense')

        # conjugate verb depending on infinitive ending
        if session.get('infinitive').endswith('ar'):
            session['correct_answer'] = conjugate_ar(infinitive, subj)
        if session.get('infinitive').endswith('er'):
            session['correct_answer'] = conjugate_er(infinitive, subj)
        if session.get('infinitive').endswith('ir'):
            session['correct_answer'] = conjugate_ir(infinitive, subj)

    return render_template('practice_view.html', title=active_set,
                           correct_answer=session.get('correct_answer'),
                           infinitive=session.get('infinitive'),
                           subject=subj,
                           tense=tense,
                           correct=session.get('correct'),
                           incorrect=session.get('incorrect'))


if __name__ == '__main__':
    app.run(debug=True)
