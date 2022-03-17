from re import search

def substr(en_string, exp):
    if en_string:
        s_result = search(exp, en_string)
        return s_result[0]
    else:
        return en_string