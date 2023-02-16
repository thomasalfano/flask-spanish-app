import string


def parse_text(form_data):
    """
    Text Processing for form input
    :param form_data: text-data from forms used in the app
    :return: list of words, seperated by white-space, stripped of punctuation
    """
    form_split = form_data.split()
    stripped_list = [word.strip(string.punctuation) for word in form_split]
    for i in range(len(stripped_list)):
        stripped_list[i] = stripped_list[i].lower()
        i += 1
    return stripped_list


if __name__ == '__main__':
    pass
