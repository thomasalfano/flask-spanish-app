from flask import render_template, url_for, current_app, redirect, session, flash, request
from flask_login import login_required

from .. import db
from ..models import Stems
from . import main
from .forms import UnknownInfForm, CreateSetForm, InfinitiveForm, TypeForm, IrregularForm
from ..view_helpers import *
from ..conjugations import *
import random


@main.route('/')
def index():
    return redirect(url_for('main.practice_select'))


# verb view function that shows all infinitives in the db, grouped into their respective categories
# add infinitive to list upon successful verb_form completion
@main.route('/verb-view', methods=['POST', 'GET'])
@login_required
def verb_view():
    """
    View Function for adding verbs/infinitives to the database.

    :return: Display tables for verbs of every type, and the verb_form used to add to those tables, if already exists,
    and is attempted to be added, flash a message
    """
    form = InfinitiveForm()
    infinitives_list = Verb.query.all()
    existing_verbs = []
    verb_forms = ['ar verbs', 'er verbs', 'ir verbs', 'irregular']
    form.form.choices = verb_forms

    if form.validate_on_submit():
        infin_list = parse_text(form.infinitive.data)

        if form.stem_changer.data:
            stem_changer = form.stem_changer.data[0]
        else:
            stem_changer = None

        # add everything from text-field input
        for verb in infin_list:
            existing_verb = Verb.query.filter_by(infinitive=verb).first()

            if not existing_verb:
                if stem_changer:
                    form_infin = verb
                    verb_form = db.session.query(VerbForm).filter_by(verb_form=form.form.data).first()
                    stem = db.session.query(Stems).filter_by(stem=stem_changer).first()
                    new_verb = Verb(infinitive=form_infin, verb_form=verb_form, stem=stem)
                    db.session.add(new_verb)

                else:
                    form_infin = verb
                    verb_form = db.session.query(VerbForm).filter_by(verb_form=form.form.data).first()
                    new_verb = Verb(infinitive=form_infin, verb_form=verb_form)
                    db.session.add(new_verb)

            else:
                flash('This infinitive exists already', category='message')
                existing_verbs.append(existing_verb)
        form.infinitive.data = ''  # clears all verb_form data after completion
        form.form.data = ''

        db.session.commit()

        infinitives_list = Verb.query.all()

        return render_template('verb_view.html', infinitives_list=infinitives_list, form=form,
                               verb_forms=verb_forms, existing_verbs=existing_verbs)
    else:
        return render_template('verb_view.html', infinitives_list=infinitives_list, form=form,
                               verb_forms=verb_forms, existing_verbs=existing_verbs)


@main.route('/setup', methods=['GET', 'POST'])
@login_required
def setup():
    """
    View Function for practice set creation.

    Function waits for a POST request from set_form or unknown_inf_form, when one of these condition is met, any data
    that was included in the verb_form will be added to the appropriate database table

    Forms
    _____

    set_form - this form is used to acquire all the details needed to create a practice set, including:
        * title
        * subjects to be prompted (singular, plural, formal)
        * the tense(s) to be used in the set
        * any preset lists of verbs that should be included (ex: all ar verbs)
        * custom text box for adding specific verbs

    unknown_inf_form - this form shows up when the user tries to create a practice set with infinitives that are not
    already in the database.

        * text box with the unknown infinitive(s)
        * drop down for which type
        * check boxes for specifying stem-change behavior if needed




    Unknown Infinitives
    ________________________

    If any of the fields of set_form return an infinitive/verb that is not already in the database, it will get appended
    to a list "unknown_infinitives" which is used to create an UnknownInfForm that is used to help gather more
    information so that the verbs can be added correctly.

    :return: Displays verb_form used to create practice sets, display pop-up window for unrecognized verbs.
    """

    set_form = CreateSetForm()
    unknown_inf_form = UnknownInfForm()
    tense_choices = Tense.query.all()
    set_form.tenses.choices = [str(i) for i in tense_choices]
    unknown_infinitives = []
    session['unknowns'] = False         # this session variable is used to determine if the unknown infinitive form
                                        # needs to show up

    if session.get('ar verbs') is None:
        query_ar = VerbForm.query.filter_by(verb_form='ar verbs').first()
        session['ar verbs'] = query_ar.verb_form
        ar_verbs = session.get('ar verbs')
        query_er = VerbForm.query.filter_by(verb_form='er verbs').first()
        session['er verbs'] = query_er.verb_form
        er_verbs = session.get('er verbs')
        query_ir = VerbForm.query.filter_by(verb_form='ir verbs').first()
        session['ir verbs'] = query_ir.verb_form
        ir_verbs = session.get('ir verbs')
        query_irreg = VerbForm.query.filter_by(verb_form='irregular').first()
        session['irregular verbs'] = query_irreg.verb_form
        irregular_verbs = session.get('irregular verbs')

    else:
        ar_verbs = session.get('ar verbs')
        er_verbs = session.get('er verbs')
        ir_verbs = session.get('ir verbs')
        irregular_verbs = session.get('irregular verbs')

    set_form.verb_type.choices = [ar_verbs, ir_verbs, er_verbs, irregular_verbs, 'o to ue', 'e to i', 'e to ie']

    if request.method == 'POST' and set_form.submit1.data is True:
        existing_set = db.session.query(Practice_Set).filter_by(label=set_form.title.data).first()

        if not existing_set:
            create_practice_set(set_form.data)

            query_set = db.session.query(Practice_Set).filter_by(label=set_form.title.data).first()
            session['title'] = set_form.title.data
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
                print(unknown_infinitives)

            if len(unknown_infinitives) > 0:

                session['unknowns'] = True

                for unknown_inf in unknown_infinitives:
                    type_form = TypeForm()
                    type_form.verb = unknown_inf

                    unknown_inf_form.unknown_verb.append_entry(type_form)
            else:
                return redirect(url_for('main.practice_select'))

    if request.method == 'POST' and unknown_inf_form.submit2.data is True:
        data = unknown_inf_form.unknown_verb.data

        add_unknown_infinitives(data, session.get('title'))

        return redirect(url_for('main.practice_select'))

    return render_template('setup.html', unknowns=session.get('unknowns'),
                           unknown_infinitives=unknown_infinitives,
                           forms=VerbForm.query.all(),
                           form=set_form,
                           unknown_inf_form=unknown_inf_form)


@main.route('/practice-select', methods=['GET', 'POST'])
def practice_select():
    """ View Function for selecting which set to be practiced.

        Displays all the practice sets that exist in the database

    :return: displays all practice-sets from the database
    """

    practice_sets = Practice_Set.query.all()
    return render_template('practice_select.html', practice_sets=practice_sets)


@main.route('/practice/<active_set>', methods=['GET', 'POST'])
def practice(active_set):
    """
    View function for student practice interaction.
    :param active_set: The set that was selected for practicing

    :return: displays random prompts using verbs, subjects, and tenses associated with the active_set.
    """

    if session.get('set') != active_set:  # if the sessions set has not been set, or has changed, update lists
        session['set'] = active_set
        query_set = db.session.query(Practice_Set).filter_by(label=session.get('set')).first()
        session['set_id'] = query_set.id
        set_id = session.get('set_id')

        infin_query = db.session.query(SetVerbs).filter_by(set_id=set_id).all()
        session['infinitives_list'] = [infin.verb.infinitive for infin in infin_query]
        session['infinitive_forms_list'] = [infin.verb.verbForm_id for infin in infin_query]
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

        target_infin = random.choice(infinitives_list)
        idx = infinitives_list.index(target_infin)
        target_form_id = infinitive_forms[idx]
        target_infin_id = infinitive_ids[idx]
        target_stem_id = infinitive_stems[idx]
        target_subj = random.choice(subjects)
        target_tense = random.choice(available_tenses)

        session['infinitive'] = target_infin
        session['subj'] = target_subj
        session['tense'] = target_tense
        infinitive = session.get('infinitive')
        subj = session.get('subj')
        irr_form = VerbForm.query.filter_by(verb_form='irregular').first()

        tense = session.get('tense')

        if target_form_id != irr_form.id:  # check what type the target verb is, and conjugate with matching function
            if infinitive.endswith('ar') and target_stem_id is None:
                session['correct_answer'] = conjugate_regular_ar(target_infin, target_subj)

            if infinitive.endswith('er') and target_stem_id is None:
                session['correct_answer'] = conjugate_regular_er(target_infin, target_subj)

            if infinitive.endswith('ir') and target_stem_id is None:
                session['correct_answer'] = conjugate_regular_ir(target_infin, target_subj)

            if target_stem_id == 3 and infinitive.endswith('ir'):
                session['correct_answer'] = conjugate_ir_e_to_i(target_infin, target_subj)

            if target_stem_id == 2:
                if infinitive.endswith('ar'):
                    session['correct_answer'] = conjugate_ar_e_to_ie(target_infin, target_subj)

                elif infinitive.endswith('er'):

                    session['correct_answer'] = conjugate_er_e_to_ie(target_infin, target_subj)

                elif infinitive.endswith('ir'):

                    session['correct_answer'] = conjugate_ir_e_to_ie(target_infin, target_subj)

            if target_stem_id == 1:
                if infinitive.endswith('ar'):
                    session['correct_answer'] = conjugate_ar_o_to_ue(target_infin, target_subj)

                elif infinitive.endswith('er'):

                    session['correct_answer'] = conjugate_er_o_to_ue(target_infin, target_subj)

                elif infinitive.endswith('ir'):

                    session['correct_answer'] = conjugate_ir_o_to_ue(target_infin, target_subj)

        else:  # use db for lookup of irregular verbs

            session['correct_answer'] = conjugate_irregular(target_subj, target_infin_id)

        return render_template('practice_view.html', title=active_set,
                               correct_answer=session.get('correct_answer'),
                               infinitive=session.get('infinitive'),
                               subject=subj,
                               tense=tense,
                               correct=session.get('correct'),
                               incorrect=session.get('incorrect'))


@main.route('/add-irregular', methods=['GET', 'POST'])
@login_required
def add_irregular():
    """ View function for adding irregular verbs to the databases.

    :return: displays a small table of verbs that have the verb_form of 'irregular',
     along with a form for adding their conjugations.
    """

    form = IrregularForm()
    ir_form_id = VerbForm.query.filter_by(verb_form='irregular').first()
    infins = Verb.query.filter_by(verb_form=ir_form_id).all()

    if form.validate_on_submit():
        infin = Verb.query.filter_by(infinitive=form.ir_infin.data).first()

        if infin is None:
            new_verb = form.ir_infin.data
            new_form = VerbForm.query.filter_by(verb_form='irregular').first()
            add_verb = Verb(infinitive=new_verb, verb_form=new_form)
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
