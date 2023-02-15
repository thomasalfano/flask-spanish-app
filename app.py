from flask import Flask, render_template, redirect, url_for, request, session, flash
from wtforms.form import BaseForm
from wtforms import SelectField
import random
from db_setup import db, Verb, SetVerbs, SetTenses, Form, Subject, Practice_Set, Tense, IrregularConjugation
from conjugate import conjugate_ar, conjugate_ir, conjugate_er, parse_text
from forms import InfinitiveForm, CreateSetForm, ConfirmForm, IrregularForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimZfAb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres::@localhost/flask_spanish'

# initialize db with app instance
db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


# verb view function that shows all infinitives in the db, grouped into their respective categories
# add infinitive to list upon successful form completion
@app.route('/verb-view', methods=['POST', 'GET'])
def verb_view():
    form = InfinitiveForm()
    infinitives_list = Verb.query.all()
    verb_forms = Form.query.all()
    form.form.choices = verb_forms

    # if form validates, query the verb table using form data
    # add new entry if verb does not exist
    if form.validate_on_submit():
        infin_list = parse_text(form.infinitive.data)
        print(infin_list)

        # add everything from text-field input
        for verb in infin_list:
            existing_verb = Verb.query.filter_by(infinitive=verb).first()

            # if not an existing verb in db
            # add new verb to db using form data
            if not existing_verb:
                form_infin = verb
                verb_form = db.session.query(Form).filter_by(form=form.form.data).first()
                new_verb = Verb(infinitive=form_infin, form=verb_form)
                db.session.add(new_verb)
            else:
                flash('This infinitive exists already', category='message')
                return render_template('verb_view.html', infinitives_list=infinitives_list, form=form)

        # clear form data after successful entry
        form.infinitive.data = ''
        form.form.data = ''
        # commit all the new additions to the db
        db.session.commit()
        infinitives_list = Verb.query.all()
        return render_template('verb_view.html', infinitives_list=infinitives_list, form=form, verb_forms=verb_forms)
    else:
        return render_template('verb_view.html', infinitives_list=infinitives_list, form=form, verb_forms=verb_forms)


# setup route for creating 'practice sets'
@app.route('/setup', methods=['GET', 'POST'])
def setup():
    # variables to be used in html templates
    form = CreateSetForm()
    unknown_inf_form = None
    tense_choices = Tense.query.all()
    form.tenses.choices = [str(i) for i in tense_choices]
    unknown_infinitives = []
    session['exists'] = True

    # query the ar verbs for form checkbox
    ar_verbs = Form.query.filter_by(form='ar verbs').first()
    er_verbs = Form.query.filter_by(form='er verbs').first()
    ir_verbs = Form.query.filter_by(form='ir verbs').first()

    # fill form choices
    form.verb_type.choices = [ar_verbs.form, ir_verbs.form, er_verbs.form]

    if form.validate_on_submit():
        set_title = form.title.data
        tenses = form.tenses.data
        preset_list = form.verb_type.data
        infinitives = parse_text(form.infinitives.data)

        # clear form entry
        form.title.data = ''
        form.tenses.data = ''
        form.infinitives.data = ''

        # add new practice set title to practice_set table if not found in query
        existing_set = Practice_Set.query.filter_by(label=form.title.data).first()
        if not existing_set:
            new_set = Practice_Set(label=set_title)
            db.session.add(new_set)
            db.session.commit()

            # query the addition that was just made
            query_set = db.session.query(Practice_Set).filter_by(label=set_title).first()

            # checks for form input from the custom infinitives box
            if infinitives:
                # for infinitives selected in form, add to set_verbs
                # EX:
                #    set_id    verb_id
                #       1          2
                #       1          3
                for infin in infinitives:
                    # query the infinitive
                    query_infin = Verb.query.filter_by(infinitive=infin).first()

                    # if the query returns an infinitive, add it to the set table with corresponding set id
                    if query_infin:
                        set_infin = SetVerbs(verb=query_infin, practice_set=query_set)
                        db.session.add(set_infin)

                    # if the query returns none, return pop-up window to add the infinitive(s) to the db
                    if not query_infin:
                        unknown_infinitives.append(infin)
                        session['exists'] = False

                # repeat above step for tenses
                for i in tenses:
                    # query the tense
                    query_tense = Tense.query.filter_by(tense=i).first()

                    set_tense = SetTenses(tense=query_tense, practice_set=query_set)
                    db.session.add(set_tense)
                db.session.commit()

            # add preset verb list if any boxes are checked
            if preset_list:
                # for all boxes checked, add verbs with that corresponding type
                for form in preset_list:
                    query_form = Form.query.filter_by(form=form).first()
                    query_verbs = Verb.query.filter_by(form=query_form).all()
                    for verb in query_verbs:
                        set_infin = SetVerbs(verb=verb, practice_set=query_set)
                        db.session.add(set_infin)
                    # repeat above step for tenses
                    for i in tenses:
                        # query the tense
                        query_tense = Tense.query.filter_by(tense=i).first()

                        set_tense = SetTenses(tense=query_tense, practice_set=query_set)
                        db.session.add(set_tense)
                db.session.commit()
            dropdown_dict = {}
            forms = Form.query.all()
            for inf in unknown_infinitives:
                dropdown_dict[inf] = SelectField(forms)
            unknown_inf_form = BaseForm(dropdown_dict)
        return render_template('setup.html', exists=session.get('exists'),
                               unknown_infinitives=unknown_infinitives,
                               forms=Form.query.all(),
                               form=CreateSetForm(),
                               unknown_inf_form=unknown_inf_form)

    if request.method == 'POST':

        print(confirm_form.form.data)

        return render_template('setup.html', exists=session.get('exists'),
                               unknown_infinitives=unknown_infinitives,
                               forms=Form.query.all(),
                               form=CreateSetForm(),
                               confirm_form=confirm_form)

        # TODO: program db adding of unknown infins from infin form data

    else:
        return render_template('setup.html', form=form, exists=session.get('exists'),
                               unknown_infinitives=unknown_infinitives,
                               forms=Form.query.all())


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
    available_infinitives = db.session.query(SetVerbs).filter_by(set_id=query_set.id).all()
    available_tenses = db.session.query(SetTenses).filter_by(set_id=query_set.id).all()
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

        session['infinitive'] = rand_infin.verb.infinitive
        session['subj'] = rand_subj.subject
        session['tense'] = rand_tense.tense.tense
        infinitive = session.get('infinitive')
        subj = session.get('subj')
        irr_form = Form.query.filter_by(form='irregular').first()
        tense = session.get('tense')

        # conjugate verb through function if function not irregular
        if rand_infin.verb.form_id != irr_form.id:
            if session.get('infinitive').endswith('ar'):
                session['correct_answer'] = conjugate_ar(infinitive, subj)
            if session.get('infinitive').endswith('er'):
                session['correct_answer'] = conjugate_er(infinitive, subj)
            if session.get('infinitive').endswith('ir'):
                session['correct_answer'] = conjugate_ir(infinitive, subj)

        # use db lookup for conjugation
        else:

            query_irr = IrregularConjugation.query.filter_by(infin_id=rand_infin.verb.id).first()
            if session.get('subj') == 'yo':
                session['correct_answer'] = query_irr.yo
            elif session.get('subj') == 'tu':
                session['correct_answer'] = query_irr.tu
            elif session.get('subj') == 'el':
                session['correct_answer'] = query_irr.el
            elif session.get('subj') == 'ella':
                session['correct_answer'] = query_irr.ella
            elif session.get('subj') == 'usted':
                session['correct_answer'] = query_irr.usted
            elif session.get('subj') == 'nosotros':
                session['correct_answer'] = query_irr.nosotros
            elif session.get('subj') == 'nosotras':
                session['correct_answer'] = query_irr.nosotras
            elif session.get('subj') == 'ellos':
                session['correct_answer'] = query_irr.ellos
            elif session.get('subj') == 'ellas':
                session['correct_answer'] = query_irr.ellas
            elif session.get('subj') == 'ustedes':
                session['correct_answer'] = query_irr.ustedes

        return render_template('practice_view.html', title=active_set,
                               correct_answer=session.get('correct_answer'),
                               infinitive=session.get('infinitive'),
                               subject=subj,
                               tense=tense,
                               correct=session.get('correct'),
                               incorrect=session.get('incorrect'))


# page for adding irregular, non pattern-following verbs
@app.route('/add-irregular', methods=['GET', 'POST'])
def add_irregular():
    form = IrregularForm()
    ir_form_id = Form.query.filter_by(form='irregular').first()
    infins = Verb.query.filter_by(form=ir_form_id).all()

    if form.validate_on_submit():
        infin = Verb.query.filter_by(infinitive=form.ir_infin.data).first()

        new_conjugation = IrregularConjugation(infin_id=infin.id, yo=form.yo_form.data, tu=form.tu_form.data,
                                               el=form.el_form.data, ella=form.ella_form.data,
                                               usted=form.usted_form.data,
                                               nosotros=form.nosotros_form.data,
                                               nosotras=form.nosotras_form.data,
                                               ellos=form.ellos_form.data,
                                               ellas=form.ellas_form.data, ustedes=form.ustedes_form.data
                                               )
        db.session.add(new_conjugation)
        db.session.commit()
        return redirect(url_for('add_irregular'))
    return render_template('add_irregular.html', form=form, infins=infins)


if __name__ == '__main__':
    app.run(debug=True)
