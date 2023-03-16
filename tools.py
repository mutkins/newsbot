import re
import requests


def is_string_equal(str1, str2):
    # Checking that string are equal general (regardless special marks, dots, other symbols)
    str1_cmsd_list = re.findall(r"[А-я\w]", str1)
    str1_cmsd_string = ''.join(str1_cmsd_list)

    str2_cmsd_list = re.findall(r"[А-я\w]", str2)
    str2_cmsd_string = ''.join(str2_cmsd_list)

    if str1_cmsd_string == str2_cmsd_string:
        return True
    else:
        return False


def is_string_exist_in_list(title, sent_news_list):
    for i in sent_news_list:
        str1_cmsd_list = re.findall(r"[А-я\w]", title)
        str1_cmsd_string = ''.join(str1_cmsd_list)

        str2_cmsd_list = re.findall(r"[А-я\w]", i)
        str2_cmsd_string = ''.join(str2_cmsd_list)

        if str1_cmsd_string == str2_cmsd_string:
            return True
    return False


def get_original_url_of_news(url):
    res = requests.get(url)
    return res.url
