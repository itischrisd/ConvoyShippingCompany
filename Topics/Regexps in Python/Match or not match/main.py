import re


def matched(template, string):
    if re.match(template, string) is not None:
        return True
    else:
        return False