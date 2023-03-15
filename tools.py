import re


def is_string_equal(str1, str2):
    # Checking that string are equal general (regardless special marks, dots, other symbols)
    if re.search(r'[А-я]|\w', str1).group(0) == re.search(r'[А-я]|\w', str2).group(0):
        return True
    else:
        return False


def is_string_exist_in_list(title, sent_news_list):
    for i in sent_news_list:
        if re.search(r'[А-я]|\w', title).group(0) == re.search(r'[А-я]|\w', i).group(0):
            return True
    return False
