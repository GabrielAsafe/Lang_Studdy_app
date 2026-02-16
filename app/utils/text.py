import re


def clean_word(palavra):
    return re.sub(r"[^\w]", "", palavra)


