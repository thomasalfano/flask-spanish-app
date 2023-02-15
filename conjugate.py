import string


def conjugate_ar(infin, subj):
    if subj == 'yo':
        return infin[:-2] + 'o'
    elif subj == 'tu':
        return infin[:-2] + 'as'
    elif subj == 'el' or 'ella' or 'usted':
        return infin[:-2] + 'a'
    elif subj == 'nosotros':
        return infin[:-2] + 'amos'
    elif subj == 'vosotros':
        return infin[:-2] + 'ais'
    elif subj == 'ellos' or 'ellas' or 'ustedes':
        return infin[:-2] + 'an'


def conjugate_er(infin, subj):
    if subj == 'yo':
        return infin[:-2] + 'o'
    elif subj == 'tu':
        return infin[:-2] + 'es'
    elif subj == 'el' or 'ella' or 'usted':
        return infin[:-2] + 'e'
    elif subj == 'nosotros':
        return infin[:-2] + 'emos'
    elif subj == 'vosotros':
        return infin[:-2] + 'eis'
    elif subj == 'ellos' or 'ellas' or 'ustedes':
        return infin[:-2] + 'en'


def conjugate_ir(infin, subj):
    if subj == 'yo':
        return infin[:-2] + 'o'
    elif subj == 'tu':
        return infin[:-2] + 'es'
    elif subj == 'el' or 'ella' or 'usted':
        return infin[:-2] + 'e'
    elif subj == 'nosotros':
        return infin[:-2] + 'imos'
    elif subj == 'vosotros':
        return infin[:-2] + 'is'
    elif subj == 'ellos' or 'ellas' or 'ustedes':
        return infin[:-2] + 'en'


def parse_text(form_data):

    form_split = form_data.split()
    stripped_list = [word.strip(string.punctuation) for word in form_split]
    for i in range(len(stripped_list)):
        stripped_list[i] = stripped_list[i].lower()
        i += 1
    return stripped_list


if __name__ == '__main__':
    pass
