from .models import db
from .models import Practice_Set, SetSubjects, SetVerbs, SetTenses, Subject, Tense, Verb, VerbForm
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
