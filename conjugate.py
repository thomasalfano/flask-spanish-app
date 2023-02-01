def conjugate_ar(infin, subj):
    if subj == 'yo':
        return infin[:-2] + 'o'
    elif subj == 'tu':
        return infin[:-2] + 'as'
    elif subj == 'el/ella/usted':
        return infin[:-2] + 'a'
    elif subj == 'nosotros':
        return infin[:-2] + 'amos'
    elif subj == 'vosotros':
        return infin[:-2] + 'ais'
    elif subj == 'ellos/ellas/ustedes':
        return infin[:-2] + 'an'


def conjugate_er(infin, subj):
    if subj == 'yo':
        return infin[:-2] + 'o'
    elif subj == 'tu':
        return infin[:-2] + 'es'
    elif subj == 'el/ella/usted':
        return infin[:-2] + 'e'
    elif subj == 'nosotros':
        return infin[:-2] + 'emos'
    elif subj == 'vosotros':
        return infin[:-2] + 'eis'
    elif subj == 'ellos/ellas/ustedes':
        return infin[:-2] + 'en'


def conjugate_ir(infin, subj):
    if subj == 'yo':
        return infin[:-2] + 'o'
    elif subj == 'tu':
        return infin[:-2] + 'es'
    elif subj == 'el/ella/usted':
        return infin[:-2] + 'e'
    elif subj == 'nosotros':
        return infin[:-2] + 'imos'
    elif subj == 'vosotros':
        return infin[:-2] + 'is'
    elif subj == 'ellos/ellas/ustedes':
        return infin[:-2] + 'en'


if __name__ == '__main__':
    pass
