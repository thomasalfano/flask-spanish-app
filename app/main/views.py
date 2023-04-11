from flask import render_template, url_for, current_app, redirect, session, flash, request
from .. import db
from ..models import Stems
from . import main
from .forms import UnknownInfForm, CreateSetForm, InfinitiveForm, TypeForm, IrregularForm
from ..helpers import *
import random


@main.route('/')
def index():
    return render_template('index.html')


# verb view function that shows all infinitives in the db, grouped into their respective categories
# add infinitive to list upon successful form completion
@main.route('/verb-view', methods=['POST', 'GET'])
def verb_view():
    """
    View Function for adding verbs/infinitives to the database.

    :return: Display tables for verbs of every type, and the form used to add to those tables
    """
    VerbForm = InfinitiveForm()
    infinitives_list = Verb.query.all()
    verb_forms = ['ar verbs', 'er verbs', 'ir verbs', 'irregular']
    VerbForm.form.choices = verb_forms

    # if form validates, query the verb table using form data
    # add new entry if verb does not exist
    if VerbForm.validate_on_submit():
        infin_list = parse_text(VerbForm.infinitive.data)

        if VerbForm.stem_changer.data:
            stem_changer = VerbForm.stem_changer.data[0]
        else:
            stem_changer = None

        # add everything from text-field input
        for verb in infin_list:
            existing_verb = Verb.query.filter_by(infinitive=verb).first()

            # if not an existing verb in db
            # add new verb to db using form data
            if not existing_verb:
                if stem_changer:
                    form_infin = verb
                    verb_form = db.session.query(Form).filter_by(form=VerbForm.form.data).first()
                    stem = db.session.query(Stems).filter_by(stem=stem_changer).first()
                    new_verb = Verb(infinitive=form_infin, form=verb_form, stem=stem)
                    db.session.add(new_verb)

                else:
                    form_infin = verb
                    verb_form = db.session.query(Form).filter_by(form=VerbForm.form.data).first()
                    new_verb = Verb(infinitive=form_infin, form=verb_form)
                    db.session.add(new_verb)

            else:
                flash('This infinitive exists already', category='message')
                return render_template('verb_view.html', infinitives_list=infinitives_list, form=VerbForm)

        # clear form data after successful entry
        VerbForm.infinitive.data = ''
        VerbForm.form.data = ''
        # commit all the new additions to the db
        db.session.commit()
        infinitives_list = Verb.query.all()
        return render_template('verb_view.html', infinitives_list=infinitives_list, form=VerbForm,
                               verb_forms=verb_forms)
    else:
        return render_template('verb_view.html', infinitives_list=infinitives_list, form=VerbForm,
                               verb_forms=verb_forms)


# setup route for creating 'practice sets'
@main.route('/setup', methods=['GET', 'POST'])
def setup():
    """
    View Function for practice set creation.

    :return: Displays form used to create practice sets, display pop-up window for unrecognized verbs.
    """

    # variables to be used in html templates
    set_form = CreateSetForm()
    unknown_inf_form = UnknownInfForm()
    tense_choices = Tense.query.all()
    set_form.tenses.choices = [str(i) for i in tense_choices]
    unknown_infinitives = []
    session['exists'] = True

    # query the ar verbs for form checkbox
    if session.get('ar verbs') is None:
        query_ar = Form.query.filter_by(form='ar verbs').first()
        session['ar verbs'] = query_ar.form
        ar_verbs = session.get('ar verbs')
        query_er = Form.query.filter_by(form='er verbs').first()
        session['er verbs'] = query_er.form
        er_verbs = session.get('er verbs')
        query_ir = Form.query.filter_by(form='ir verbs').first()
        session['ir verbs'] = query_ir.form
        ir_verbs = session.get('ir verbs')
        query_irreg = Form.query.filter_by(form='irregular').first()
        session['irregular verbs'] = query_irreg.form
        irregular_verbs = session.get('irregular verbs')

    else:
        ar_verbs = session.get('ar verbs')
        er_verbs = session.get('er verbs')
        ir_verbs = session.get('ir verbs')
        irregular_verbs = session.get('irregular verbs')

    # fill form choices
    set_form.verb_type.choices = [ar_verbs, ir_verbs, er_verbs, irregular_verbs, 'o to ue', 'e to i', 'e to ie']

    # check if the incoming POST request comes from the setup form
    if request.method == 'POST' and set_form.submit1.data is True:
        existing_set = db.session.query(Practice_Set).filter_by(label=set_form.title.data).first()

        if not existing_set:
            create_practice_set(set_form.data)

            query_set = db.session.query(Practice_Set).filter_by(label=set_form.title.data).first()

            tenses = set_form.tenses.data
            if tenses:
                add_set_tenses(tenses, query_set)

            subjects = set_form.subject.data
            if subjects:
                add_set_subjects(subjects, query_set)

            preset_list = set_form.verb_type.data
            if preset_list:
                add_preset_lists(set_form.verb_type.data, query_set, tenses)

            infinitives = set_form.infinitives.data
            if infinitives:
                unknown_infinitives = add_infinitives(set_form.infinitives.data, query_set)

            if unknown_infinitives:

                for unknown_inf in unknown_infinitives:
                    type_form = TypeForm()
                    type_form.verb = unknown_inf

                    unknown_inf_form.unknown_verb.append_entry(type_form)
            else:
                return redirect(url_for('main.practice_select'))

    # check if the incoming POST request is coming from the unknown_inf_form
    if request.method == 'POST' and unknown_inf_form.submit2.data is True:
        data = unknown_inf_form.unknown_verb.data

        # for each verb in the form, add that verb and its type to the db
        for idx, verb in enumerate(data):
            verb = data[idx]['verb']
            v_type = data[idx]['type']
            if data[idx]['stem_changer']:  # check if form gave stem changer data
                v_stem = data[idx]['stem_changer'][0]
            else:
                v_stem = None
            if v_stem is None:
                verb_form = db.session.query(Form).filter_by(form=v_type).first()
                new_verb = Verb(infinitive=verb, form=verb_form)
                db.session.add(new_verb)
            else:
                verb_form = db.session.query(Form).filter_by(form=v_type).first()
                stem = db.session.query(Stems).filter_by(stem=v_stem).first()
                new_verb = Verb(infinitive=verb, form=verb_form, stem=stem)
                db.session.add(new_verb)

        db.session.commit()

        # now that this verb exists in the db, we will add all of them to the db with the associated practice set
        for idx, verb in enumerate(data):
            infinitive = data[idx]['verb']
            set_title = session.get('title')
            query_infin = Verb.query.filter_by(infinitive=infinitive).first()
            query_set = Practice_Set.query.filter_by(label=set_title).first()
            set_infin = SetVerbs(verb=query_infin, practice_set=query_set)
            db.session.add(set_infin)
        db.session.commit()

        return redirect(url_for('main.practice_select'))

    return render_template('setup.html', exists=session.get('exists'),
                           unknown_infinitives=unknown_infinitives,
                           forms=Form.query.all(),
                           form=set_form,
                           unknown_inf_form=unknown_inf_form)


# route for selecting which 'practice set' to be used
@main.route('/practice-select', methods=['GET', 'POST'])
def practice_select():
    """
    View Function for selecting what set to use for practice.
    :return: displays all practice-sets from the database
    """
    practice_sets = Practice_Set.query.all()
    return render_template('practice_select.html', practice_sets=practice_sets)


# student facing practice screen that uses conjugation function to check student answers for correctness
@main.route('/practice/<active_set>', methods=['GET', 'POST'])
def practice(active_set):
    """
    View function for student practice interaction.
    :param active_set: The set selected for practicing
    :return: displays random prompts using verbs, subjects, and tenses associated with the active_set.
    """

    # check if the session's set has changed/exists
    # if changed/does not exist, do all the database querying
    if session.get('set') != active_set:
        session['set'] = active_set
        query_set = db.session.query(Practice_Set).filter_by(label=session.get('set')).first()
        session['set_id'] = query_set.id
        set_id = session.get('set_id')

        infin_query = db.session.query(SetVerbs).filter_by(set_id=set_id).all()
        session['infinitives_list'] = [infin.verb.infinitive for infin in infin_query]
        session['infinitive_forms_list'] = [infin.verb.form_id for infin in infin_query]
        session['infinitive_stem_id'] = [infin.verb.stem_id for infin in infin_query]
        session['infinitive_ids_list'] = [infin.verb.id for infin in infin_query]
        infinitives_list = session.get('infinitives_list')
        infinitive_forms = session.get('infinitive_forms_list')
        infinitive_ids = session.get('infinitive_ids_list')
        infinitive_stems = session.get('infinitive_stem_id')

        query_tenses = db.session.query(SetTenses).filter_by(set_id=set_id).all()
        session['tense_list'] = [tense.tense.tense for tense in query_tenses]
        available_tenses = session.get('tense_list')

        subject_query = db.session.query(SetSubjects).filter_by(set_id=set_id).all()
        session['subj_list'] = [subj.subject.subject for subj in subject_query]
        subjects = session.get('subj_list')

    # if the sessions set has not changed, keep using the same lists
    else:
        available_tenses = session.get('tense_list')
        infinitives_list = session.get('infinitives_list')
        infinitive_forms = session.get('infinitive_forms_list')
        infinitive_ids = session.get('infinitive_ids_list')
        infinitive_stems = session.get('infinitive_stem_id')
        subjects = session.get('subj_list')

    session['incorrect'] = False

    if request.method == 'POST':
        session['user_answer'] = request.form.get('answer')

        if session.get('user_answer') == session.get('correct_answer'):
            session['incorrect'] = False
            flash('correct!', category='message')
            return redirect(url_for('main.practice', active_set=active_set))
        else:
            session['incorrect'] = True

        return render_template('practice_view.html', title=active_set,
                               correct_answer=session.get('correct_answer'),
                               infinitive=session.get('infinitive'),
                               subject=session.get('subj'),
                               tense=session.get('tense'),
                               incorrect=session.get('incorrect'))

    else:
        # randomly select from infin, subj, and tense lists
        # to be used in view function for prompt
        target_infin = random.choice(infinitives_list)
        idx = infinitives_list.index(target_infin)
        target_form_id = infinitive_forms[idx]
        target_infin_id = infinitive_ids[idx]
        target_stem_id = infinitive_stems[idx]
        print(target_stem_id)
        target_subj = random.choice(subjects)
        target_tense = random.choice(available_tenses)

        session['infinitive'] = target_infin
        session['subj'] = target_subj
        session['tense'] = target_tense
        infinitive = session.get('infinitive')
        subj = session.get('subj')
        irr_form = Form.query.filter_by(form='irregular').first()

        tense = session.get('tense')

        # conjugate verb through computation if function not irregular
        # check ending of verb to get correct conjugation
        # then match the subject prompt to the correct ending
        if target_form_id != irr_form.id:
            if infinitive.endswith('ar') and target_stem_id is None:
                session['correct_answer'] = conjugate_regular_ar(target_infin, target_subj)

            if infinitive.endswith('er') and target_stem_id is None:
                session['correct_answer'] = conjugate_regular_er(target_infin, target_subj)

            if infinitive.endswith('ir') and target_stem_id is None:
                session['correct_answer'] = conjugate_regular_ir(target_infin, target_subj)

            # if stem changer is e to i, and the verb ends with ir, perform the correct conjugation
            if target_stem_id == 3 and infinitive.endswith('ir'):
                session['correct_answer'] = conjugate_ir_e_to_i(target_infin, target_subj)

            # check if verb is an e to ie stem changer, match conjugation
            if target_stem_id == 2:
                if infinitive.endswith('ar'):
                    session['correct_answer'] = conjugate_ar_e_to_ie(target_infin, target_subj)

                elif infinitive.endswith('er'):

                    session['correct_answer'] = conjugate_er_e_to_ie(target_infin, target_subj)

                elif infinitive.endswith('ir'):

                    session['correct_answer'] = conjugate_ir_e_to_ie(target_infin, target_subj)

            # check if the verb is an o to ue stem changer
            if target_stem_id == 1:
                if infinitive.endswith('ar'):
                    session['correct_answer'] = conjugate_ar_o_to_ue(target_infin, target_subj)

                elif infinitive.endswith('er'):

                    session['correct_answer'] = conjugate_er_o_to_ue(target_infin, target_subj)

                elif infinitive.endswith('ir'):

                    session['correct_answer'] = conjugate_ir_o_to_ue(target_infin, target_subj)

        # use db lookup for conjugation
        else:

            session['correct_answer'] = conjugate_irregular(target_subj, target_infin_id)

        return render_template('practice_view.html', title=active_set,
                               correct_answer=session.get('correct_answer'),
                               infinitive=session.get('infinitive'),
                               subject=subj,
                               tense=tense,
                               correct=session.get('correct'),
                               incorrect=session.get('incorrect'))


# page for adding irregular, non pattern-following verbs
@main.route('/add-irregular', methods=['GET', 'POST'])
def add_irregular():
    """
    View function for adding irregular verbs to the databases

    :return: displays a small table of verbs that have the form of 'irregular', along with a form for adding their
        conjugations.
    """
    form = IrregularForm()
    ir_form_id = Form.query.filter_by(form='irregular').first()
    infins = Verb.query.filter_by(form=ir_form_id).all()

    if form.validate_on_submit():
        infin = Verb.query.filter_by(infinitive=form.ir_infin.data).first()

        if infin is None:
            new_verb = form.ir_infin.data
            new_form = Form.query.filter_by(form='irregular').first()
            add_verb = Verb(infinitive=new_verb, form=new_form)
            db.session.add(add_verb)
            db.session.commit()

            infin = Verb.query.filter_by(infinitive=form.ir_infin.data).first()

        else:
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

        return redirect(url_for('main.add_irregular'))
    return render_template('add_irregular.html', form=form, infins=infins)
