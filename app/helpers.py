from .models import db
from .models import IrregularConjugation, Practice_Set, SetSubjects, SetVerbs, SetTenses, Subject, Tense, Verb, Form
from text_process import parse_text


def conjugate_regular_ar(verb, subject):
    conjugated_verb = None
    match subject:
        case 'yo':
            conjugated_verb = verb[:-2] + 'o'
        case 'tu':
            conjugated_verb = verb[:-2] + 'as'
        case 'el':
            conjugated_verb = verb[:-2] + 'a'
        case 'ella':
            conjugated_verb = verb[:-2] + 'a'
        case 'usted':
            conjugated_verb = verb[:-2] + 'a'
        case 'nosotros':
            conjugated_verb = verb[:-2] + 'amos'
        case 'vosotros':
            conjugated_verb = verb[:-2] + 'ais'
        case 'ellos':
            conjugated_verb = verb[:-2] + 'an'
        case 'ellas':
            conjugated_verb = verb[:-2] + 'an'
        case 'ustedes':
            conjugated_verb = verb[:-2] + 'an'

    return conjugated_verb


def conjugate_regular_er(verb, subject):
    conjugated_verb = None
    match subject:
        case 'yo':
            conjugated_verb = verb[:-2] + 'o'
        case 'tu':
            conjugated_verb = verb[:-2] + 'es'
        case 'el':
            conjugated_verb = verb[:-2] + 'e'
        case 'ella':
            conjugated_verb = verb[:-2] + 'e'
        case 'usted':
            conjugated_verb = verb[:-2] + 'e'
        case 'nosotros':
            conjugated_verb = verb[:-2] + 'emos'
        case 'vosotros':
            conjugated_verb = verb[:-2] + 'eis'
        case 'ellos':
            conjugated_verb = verb[:-2] + 'en'
        case 'ellas':
            conjugated_verb = verb[:-2] + 'en'
        case 'ustedes':
            conjugated_verb = verb[:-2] + 'en'

    return conjugated_verb


def conjugate_regular_ir(verb, subject):
    conjugated_verb = None
    match subject:
        case 'yo':
            conjugated_verb = verb[:-2] + 'o'
        case 'tu':
            conjugated_verb = verb[:-2] + 'es'
        case 'el':
            conjugated_verb = verb[:-2] + 'e'
        case 'ella':
            conjugated_verb = verb[:-2] + 'e'
        case 'usted':
            conjugated_verb = verb[:-2] + 'e'
        case 'nosotros':
            conjugated_verb = verb[:-2] + 'imos'
        case 'vosotros':
            conjugated_verb = verb[:-2] + 'is'
        case 'ellos':
            conjugated_verb = verb[:-2] + 'en'
        case 'ellas':
            conjugated_verb = verb[:-2] + 'en'
        case 'ustedes':
            conjugated_verb = verb[:-2] + 'en'

    return conjugated_verb


def conjugate_ar_o_to_ue(verb, subject):
    stem = verb[:-2]
    vow_idx = stem.rindex('o')  # finds the penultimate vowel in the verb
    conjugated_verb = None

    match subject:
        case 'yo':
            conjugated_verb = verb[:vow_idx] + 'ue' + verb[vow_idx + 1:-2] + 'o'
        case 'tu':
            conjugated_verb = verb[:vow_idx] + 'ue' + verb[vow_idx + 1:-2] + 'as'
        case 'el':
            conjugated_verb = verb[:vow_idx] + 'ue' + verb[vow_idx + 1:-2] + 'a'
        case 'ella':
            conjugated_verb = verb[:vow_idx] + 'ue' + verb[vow_idx + 1:-2] + 'a'
        case 'usted':
            conjugated_verb = verb[:vow_idx] + 'ue' + verb[vow_idx + 1:-2] + 'a'
        case 'nosotros':
            conjugated_verb = verb[:-2] + 'amos'
        case 'vosotros':
            conjugated_verb = verb[:-2] + 'ais'
        case 'ellos':
            conjugated_verb = verb[:vow_idx] + 'ue' + verb[vow_idx + 1:-2] + 'an'
        case 'ellas':
            conjugated_verb = verb[:vow_idx] + 'ue' + verb[vow_idx + 1:-2] + 'an'
        case 'ustedes':
            conjugated_verb = verb[:vow_idx] + 'ue' + verb[vow_idx + 1:-2] + 'an'

    return conjugated_verb


def conjugate_er_o_to_ue(verb, subject):
    stem = verb[:-2]
    vow_idx = stem.rindex('o')  # finds the penultimate vowel in the verb
    conjugated_verb = None

    match subject:
        case 'yo':
            conjugated_verb = verb[:vow_idx] + 'ue' + verb[vow_idx + 1:-2] + 'o'
        case 'tu':
            conjugated_verb = verb[:vow_idx] + 'ue' + verb[vow_idx + 1:-2] + 'es'
        case 'el':
            conjugated_verb = verb[:vow_idx] + 'ue' + verb[vow_idx + 1:-2] + 'e'
        case 'ella':
            conjugated_verb = verb[:vow_idx] + 'ue' + verb[vow_idx + 1:-2] + 'e'
        case 'usted':
            conjugated_verb = verb[:vow_idx] + 'ue' + verb[vow_idx + 1:-2] + 'e'
        case 'nosotros':
            conjugated_verb = verb[:-2] + 'emos'
        case 'vosotros':
            conjugated_verb = verb[:-2] + 'eis'
        case 'ellos':
            conjugated_verb = verb[:vow_idx] + 'ue' + verb[vow_idx + 1:-2] + 'en'
        case 'ellas':
            conjugated_verb = verb[:vow_idx] + 'ue' + verb[vow_idx + 1:-2] + 'en'
        case 'ustedes':
            conjugated_verb = verb[:vow_idx] + 'ue' + verb[vow_idx + 1:-2] + 'en'

    return conjugated_verb


def conjugate_ir_o_to_ue(verb, subject):
    stem = verb[:-2]
    vow_idx = stem.rindex('o')  # finds the penultimate vowel in the verb
    conjugated_verb = None

    match subject:
        case 'yo':
            conjugated_verb = verb[:vow_idx] + 'ue' + verb[vow_idx + 1:-2] + 'o'
        case 'tu':
            conjugated_verb = verb[:vow_idx] + 'ue' + verb[vow_idx + 1:-2] + 'es'
        case 'el':
            conjugated_verb = verb[:vow_idx] + 'ue' + verb[vow_idx + 1:-2] + 'e'
        case 'ella':
            conjugated_verb = verb[:vow_idx] + 'ue' + verb[vow_idx + 1:-2] + 'e'
        case 'usted':
            conjugated_verb = verb[:vow_idx] + 'ue' + verb[vow_idx + 1:-2] + 'e'
        case 'nosotros':
            conjugated_verb = verb[:-2] + 'imos'
        case 'vosotros':
            conjugated_verb = verb[:-2] + 'is'
        case 'ellos':
            conjugated_verb = verb[:vow_idx] + 'ue' + verb[vow_idx + 1:-2] + 'en'
        case 'ellas':
            conjugated_verb = verb[:vow_idx] + 'ue' + verb[vow_idx + 1:-2] + 'en'
        case 'ustedes':
            conjugated_verb = verb[:vow_idx] + 'ue' + verb[vow_idx + 1:-2] + 'en'

    return conjugated_verb


def conjugate_ar_e_to_ie(verb, subject):
    stem = verb[:-2]
    vow_idx = stem.rindex('e')  # finds the penultimate vowel in the verb
    conjugated_verb = None
    match subject:
        case 'yo':
            conjugated_verb = verb[:vow_idx] + 'ie' + verb[vow_idx + 1:-2] + 'o'
        case 'tu':
            conjugated_verb = verb[:vow_idx] + 'ie' + verb[vow_idx + 1:-2] + 'as'
        case 'el':
            conjugated_verb = verb[:vow_idx] + 'ie' + verb[vow_idx + 1:-2] + 'a'
        case 'ella':
            conjugated_verb = verb[:vow_idx] + 'ie' + verb[vow_idx + 1:-2] + 'a'
        case 'usted':
            conjugated_verb = verb[:vow_idx] + 'ie' + verb[vow_idx + 1:-2] + 'a'
        case 'nosotros':
            conjugated_verb = verb[:-2] + 'amos'
        case 'vosotros':
            conjugated_verb = verb[:-2] + 'ais'
        case 'ellos':
            conjugated_verb = verb[:vow_idx] + 'ie' + verb[vow_idx + 1:-2] + 'an'
        case 'ellas':
            conjugated_verb = verb[:vow_idx] + 'ie' + verb[vow_idx + 1:-2] + 'an'
        case 'ustedes':
            conjugated_verb = verb[:vow_idx] + 'ie' + verb[vow_idx + 1:-2] + 'an'

    return conjugated_verb


def conjugate_er_e_to_ie(verb, subject):
    stem = verb[:-2]
    vow_idx = stem.rindex('e')  # finds the penultimate vowel in the verb
    conjugated_verb = None
    match subject:
        case 'yo':
            conjugated_verb = verb[:vow_idx] + 'ie' + verb[vow_idx + 1:-2] + 'o'
        case 'tu':
            conjugated_verb = verb[:vow_idx] + 'ie' + verb[vow_idx + 1:-2] + 'es'
        case 'el':
            conjugated_verb = verb[:vow_idx] + 'ie' + verb[vow_idx + 1:-2] + 'e'
        case 'ella':
            conjugated_verb = verb[:vow_idx] + 'ie' + verb[vow_idx + 1:-2] + 'e'
        case 'usted':
            conjugated_verb = verb[:vow_idx] + 'ie' + verb[vow_idx + 1:-2] + 'e'
        case 'nosotros':
            conjugated_verb = verb[:-2] + 'emos'
        case 'vosotros':
            conjugated_verb = verb[:-2] + 'eis'
        case 'ellos':
            conjugated_verb = verb[:vow_idx] + 'ie' + verb[vow_idx + 1:-2] + 'en'
        case 'ellas':
            conjugated_verb = verb[:vow_idx] + 'ie' + verb[vow_idx + 1:-2] + 'en'
        case 'ustedes':
            conjugated_verb = verb[:vow_idx] + 'ie' + verb[vow_idx + 1:-2] + 'en'

    return conjugated_verb


def conjugate_ir_e_to_ie(verb, subject):
    stem = verb[:-2]
    vow_idx = stem.rindex('e')  # finds the penultimate vowel in the verb
    conjugated_verb = None
    match subject:
        case 'yo':
            conjugated_verb = verb[:vow_idx] + 'ie' + verb[vow_idx + 1:-2] + 'o'
        case 'tu':
            conjugated_verb = verb[:vow_idx] + 'ie' + verb[vow_idx + 1:-2] + 'es'
        case 'el':
            conjugated_verb = verb[:vow_idx] + 'ie' + verb[vow_idx + 1:-2] + 'e'
        case 'ella':
            conjugated_verb = verb[:vow_idx] + 'ie' + verb[vow_idx + 1:-2] + 'e'
        case 'usted':
            conjugated_verb = verb[:vow_idx] + 'ie' + verb[vow_idx + 1:-2] + 'e'
        case 'nosotros':
            conjugated_verb = verb[:-2] + 'imos'
        case 'vosotros':
            conjugated_verb = verb[:-2] + 'is'
        case 'ellos':
            conjugated_verb = verb[:vow_idx] + 'ie' + verb[vow_idx + 1:-2] + 'en'
        case 'ellas':
            conjugated_verb = verb[:vow_idx] + 'ie' + verb[vow_idx + 1:-2] + 'en'
        case 'ustedes':
            conjugated_verb = verb[:vow_idx] + 'ie' + verb[vow_idx + 1:-2] + 'en'

    return conjugated_verb


def conjugate_ir_e_to_i(verb, subject):
    stem = verb[:-2]
    vow_idx = stem.rindex('e')  # finds the penultimate vowel in the verb
    conjugated_verb = None
    match subject:
        case 'yo':
            conjugated_verb = verb[:vow_idx] + 'i' + verb[vow_idx + 1:-2] + 'o'
        case 'tu':
            conjugated_verb = verb[:vow_idx] + 'i' + verb[vow_idx + 1:-2] + 'es'
        case 'el':
            conjugated_verb = verb[:vow_idx] + 'i' + verb[vow_idx + 1:-2] + 'e'
        case 'ella':
            conjugated_verb = verb[:vow_idx] + 'i' + verb[vow_idx + 1:-2] + 'e'
        case 'usted':
            conjugated_verb = verb[:vow_idx] + 'i' + verb[vow_idx + 1:-2] + 'e'
        case 'nosotros':
            conjugated_verb = verb[:-2] + 'imos'
        case 'vosotros':
            conjugated_verb = verb[:-2] + 'is'
        case 'ellos':
            conjugated_verb = verb[:vow_idx] + 'i' + verb[vow_idx + 1:-2] + 'en'
        case 'ellas':
            conjugated_verb = verb[:vow_idx] + 'i' + verb[vow_idx + 1:-2] + 'en'
        case 'ustedes':
            conjugated_verb = verb[:vow_idx] + 'i' + verb[vow_idx + 1:-2] + 'en'

    return conjugated_verb


def conjugate_irregular(subject, verb_id):
    query_irr = IrregularConjugation.query.filter_by(infin_id=verb_id).first()
    conjugated_verb = None

    match subject:
        case 'yo':
            conjugated_verb = query_irr.yo
        case 'tu':
            conjugated_verb = query_irr.tu
        case 'el':
            conjugated_verb = query_irr.el
        case 'ella':
            conjugated_verb = query_irr.ella
        case 'usted':
            conjugated_verb = query_irr.usted
        case 'nosotros':
            conjugated_verb = query_irr.nosotros
        case 'nosotras':
            conjugated_verb = query_irr.nosotras
        case 'ellos':
            conjugated_verb = query_irr.ellos
        case 'ellas':
            conjugated_verb = query_irr.ellas
        case 'ustedes':
            conjugated_verb = query_irr.ustedes

    return conjugated_verb


def create_practice_set(data):
    set_title = data['title']

    existing_set = Practice_Set.query.filter_by(label=set_title).first()

    if not existing_set:
        new_set = Practice_Set(label=set_title)
        db.session.add(new_set)

    db.session.commit()

    # query_set = db.session.query(Practice_Set).filter_by(label=set_title).first()
    #
    # subjects = data['subject']
    # if subjects:
    #     add_set_subjects(subjects, query_set)
    #
    # infinitives = data['infinitives']
    # if infinitives:
    #     add_infinitives(infinitives, query_set)
    #
    # tenses = data['tenses']
    # if tenses:
    #     add_set_tenses(tenses, query_set)
    #
    # preset_list = data['verb_type']
    # if preset_list:
    #     add_preset_lists(preset_list, query_set, tenses)


def add_set_subjects(form_data, query_set):

    for subj in form_data:
        if subj == 'plural':
            # query the subject type
            query_subjects = Subject.query.filter_by(number_id=2).all()
            for subj_id in query_subjects:
                set_subject = SetSubjects(practice_set=query_set, subject=subj_id)
                db.session.add(set_subject)

        if subj == 'singular':
            query_subjects = Subject.query.filter_by(number_id=1).all()
            for subj_id in query_subjects:
                set_subject = SetSubjects(practice_set=query_set, subject=subj_id)
                db.session.add(set_subject)

        if subj == 'formal':
            query_subjects = Subject.query.filter_by(number_id=3).all()
            for subj_id in query_subjects:
                set_subject = SetSubjects(practice_set=query_set, subject=subj_id)
                db.session.add(set_subject)

    db.session.commit()


def add_set_tenses(form_data, query_set):
    tenses = form_data

    for i in tenses:
        # query the tense
        query_tense = Tense.query.filter_by(tense=i).first()

        set_tense = SetTenses(tense=query_tense, practice_set=query_set)
        db.session.add(set_tense)
    db.session.commit()


def add_infinitives(form_data, query_set):
    infinitives = parse_text(form_data)
    unknown_infinitives = []

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

    db.session.commit()

    return unknown_infinitives


def add_preset_lists(form_data, query_set, tenses):
    preset_list = form_data
    tenses = tenses

    for form in preset_list:
        if form == 'e to i':
            print()
            query_verbs = Verb.query.filter_by(stem_id=3).all()

            # add each queried verb to the db session, will be committed later on
            for verb in query_verbs:
                set_infin = SetVerbs(verb=verb, practice_set=query_set)
                db.session.add(set_infin)
            # repeat above step for tenses
            for i in tenses:
                # query the tense
                query_tense = Tense.query.filter_by(tense=i).first()

                set_tense = SetTenses(tense=query_tense, practice_set=query_set)
                db.session.add(set_tense)

        elif form == 'e to ie':
            query_verbs = Verb.query.filter_by(stem_id=2).all()
            for verb in query_verbs:
                set_infin = SetVerbs(verb=verb, practice_set=query_set)
                db.session.add(set_infin)
            # repeat above step for tenses
            for i in tenses:
                # query the tense
                query_tense = Tense.query.filter_by(tense=i).first()

                set_tense = SetTenses(tense=query_tense, practice_set=query_set)
                db.session.add(set_tense)
        elif form == 'o to ue':
            query_verbs = Verb.query.filter_by(stem_id=1).all()
            for verb in query_verbs:
                set_infin = SetVerbs(verb=verb, practice_set=query_set)
                db.session.add(set_infin)
            # repeat above step for tenses
            for i in tenses:
                # query the tense
                query_tense = Tense.query.filter_by(tense=i).first()

                set_tense = SetTenses(tense=query_tense, practice_set=query_set)
                db.session.add(set_tense)

        else:

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


