"""Verb conjugation helper

    this module helps with the conjugation of various verb types in spanish, including: Regular AR, ER, IR verbs,
    irregular verbs, stem-changing verbs such as e-i, e-ie, o-ue.
"""

from .models import IrregularConjugation


def conjugate_regular_ar(verb, subject):
    """ Used to conjugate a regular -ar ending verb

    Parameters
    __________
    verb : Verb to be conjugated.

    subject : used to match the verb to it's correct conjugation

    Returns
    _______
    verb conjugated using the provided subject
    """
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
    """ Used to conjugate a regular -er ending verb

    Parameters
    __________
    verb : Verb to be conjugated.

    subject : used to match the verb to it's correct conjugation

    Returns
    _______
    verb conjugated using the provided subject
    """

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
    """ Used to conjugate a regular -ir ending verb

    Parameters
    __________
    verb : Verb to be conjugated.

    subject : used to match the verb to it's correct conjugation

    Returns
    _______
    verb conjugated using the provided subject
    """

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
    """ Used to conjugate an o -> ue stem changing -ar ending verb

    Parameters
    __________
    verb : Verb to be conjugated.

    subject : used to match the verb to it's correct conjugation

    Returns
    _______
    verb conjugated using the provided subject
    """

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
    """ Used to conjugate an o -> ue stem changing -er ending verb

    Parameters
    __________
    verb : Verb to be conjugated.

    subject : used to match the verb to it's correct conjugation

    Returns
    _______
    verb conjugated using the provided subject
    """

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
    """ Used to conjugate an o -> ue stem changing -ir ending verb

    Parameters
    __________
    verb : Verb to be conjugated.

    subject : used to match the verb to it's correct conjugation

    Returns
    _______
    verb conjugated using the provided subject
    """

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
    """ Used to conjugate an e -> ie stem changing -ar ending verb

    Parameters
    __________
    verb : Verb to be conjugated.

    subject : used to match the verb to it's correct conjugation

    Returns
    _______
    verb conjugated using the provided subject
    """

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
    """ Used to conjugate an e -> ie stem changing -er ending verb

    Parameters
    __________
    verb : Verb to be conjugated.

    subject : used to match the verb to it's correct conjugation

    Returns
    _______
    verb conjugated using the provided subject
    """

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
    """ Used to conjugate an e -> ie stem changing -ir ending verb

    Parameters
    __________
    verb : Verb to be conjugated.

    subject : used to match the verb to it's correct conjugation

    Returns
    _______
    verb conjugated using the provided subject
    """

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
    """ Used to conjugate an e -> i stem changing -ir ending verb

    Parameters
    __________
    verb : Verb to be conjugated.

    subject : used to match the verb to it's correct conjugation

    Returns
    _______
    verb conjugated using the provided subject
    """

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
    """ Used to look up the conjugation for a verb that is irregular

    Parameters
    __________
    verb : Verb to be conjugated.

    subject : used to match the verb to it's correct conjugation

    Returns
    _______
    verb conjugated using the provided subject
    """

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
