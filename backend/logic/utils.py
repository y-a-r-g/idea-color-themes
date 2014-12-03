import re

__author__ = 'sdvoynikov'


def escape_file_name(name):
    return re.sub('[^\w\-_\. ]', ' ', name).replace(' ', '')