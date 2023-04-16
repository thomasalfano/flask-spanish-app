from .models import db
from .models import Practice_Set, SetSubjects, SetVerbs, SetTenses, Subject, Tense, Verb, VerbForm, Stems
from text_process import parse_text


def create_practice_set(data):
    """ Adds practice_set title to database if it doesn't exist yet.

        Parameters
        __________

        data - a string that will be the title of the practice set

    """
    set_title = data['title']

    existing_set = Practice_Set.query.filter_by(label=set_title).first()

    if not existing_set:
        new_set = Practice_Set(label=set_title)
        db.session.add(new_set)

    db.session.commit()


def add_set_subjects(form_data, query_set):
    """ adds subjects to SetSubjects table, all subjects are paired to their corresponding practice set """
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
    """ Adds all tenses from form_data to the SetTenses table.

        All tenses are paired with the parameter query_set

        Parameters
        __________

        form_data - the data (tenses) from any form that should be added to the database

        query_set - a query result of a Practice Set that the tenses should be added to

    """
    tenses = form_data

    for i in tenses:
        # query the tense
        query_tense = Tense.query.filter_by(tense=i).first()

        set_tense = SetTenses(tense=query_tense, practice_set=query_set)
        db.session.add(set_tense)
    db.session.commit()


def add_infinitives(form_data, query_set):
    """ Adds all infinitives from form_data to the SetInfinitives table.

            All infinitives are paired to the set that is passed in through query_set

            Parameters
            __________

            form_data - the data (infinitives) from any form that should be added to the database

            query_set - a query result of a Practice Set that the infinitives should be added to

            :returns

            unknown_infins - list of any infins that were not found in the database

        """

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
    """ Adds all infinitives from a preset list from form_data to the SetInfinitives table.

                All infinitives are paired to the set that is passed in through query_set

                Parameters
                __________

                form_data - the data (infinitives) from any form that should be added to the database

                query_set - a query result of a Practice Set that the infinitives should be added to

    """

    preset_list = form_data
    tenses = tenses

    for form in preset_list:
        if form == 'e to i':
            print()
            query_verbs = Verb.query.filter_by(stem_id=3).all()

        elif form == 'e to ie':
            query_verbs = Verb.query.filter_by(stem_id=2).all()

        elif form == 'o to ue':
            query_verbs = Verb.query.filter_by(stem_id=1).all()

        else:

            query_form = VerbForm.query.filter_by(verb_form=form).first()
            query_verbs = Verb.query.filter_by(verb_form=query_form).all()

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


def add_unknown_infinitives(unknown_infinitives, set_title):
    """ Used to add unknown infinitives to the database, and then to any connected practice sets.

    Parameters
    _________

    unknown_infinitives - list of unknown infinitives (infinitives that are not found in the db Verbs table)
                         that should be gathered from a form

    set_title - the title of the associated practice set that the unknown verbs should be connected to
    """

    data = unknown_infinitives

    for idx, verb in enumerate(data):  # for each verb in data add the verb, and it's type
        verb = data[idx]['verb']
        v_type = data[idx]['type']
        if data[idx]['stem_changer']:  # check if verb_form gave stem changer data
            v_stem = data[idx]['stem_changer'][0]
        else:
            v_stem = None
        if v_stem is None:
            verb_form = db.session.query(VerbForm).filter_by(verb_form=v_type).first()
            new_verb = Verb(infinitive=verb, verb_form=verb_form)
            db.session.add(new_verb)
        else:
            verb_form = db.session.query(VerbForm).filter_by(verb_form=v_type).first()
            stem = db.session.query(Stems).filter_by(stem=v_stem).first()
            new_verb = Verb(infinitive=verb, verb_form=verb_form, stem=stem)
            db.session.add(new_verb)

    db.session.commit()

    # now that this verb exists in the db, we will add all of them to the db with the associated practice set
    for idx, verb in enumerate(data):
        infinitive = data[idx]['verb']
        set_title = set_title
        query_infin = Verb.query.filter_by(infinitive=infinitive).first()
        query_set = Practice_Set.query.filter_by(label=set_title).first()
        print(query_set)
        set_infin = SetVerbs(verb=query_infin, practice_set=query_set)
        db.session.add(set_infin)
    db.session.commit()
