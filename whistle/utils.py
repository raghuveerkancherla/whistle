import re

alphanum_regex = re.compile('^\w+$')
def is_alphanum(string):
    if alphanum_regex.match(string):
        return True
    else:
        return False

