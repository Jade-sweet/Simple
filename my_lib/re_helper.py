import re
from functools import partial

from rest_framework.exceptions import APIException

NAME = re.compile(r'^[a-zA-Z]{10,64}$')
NICK_NAME = re.compile(r'^[a-zA-Z0-9\u4e00-\u9fa5]{2,32}$')
PASSWORD = re.compile(r'^(?=.*[0-9].*)(?=.*[\.].*)(?=.*[A-Z].*)(?=.*[a-z].*).{8,15}$')


def check_with_pattern(pattern, value, *,  hint=False):
    """使用正则表达式检查输入的值"""
    if hint:
        return '' if pattern.match(value) else f'{value} is invalid'
    else:
        return pattern.match(value)


check_name = partial(check_with_pattern, NAME)
check_nick_name = partial(check_with_pattern, NICK_NAME)
check_password = partial(check_with_pattern, PASSWORD)


class ParamsException(APIException):

    def __init__(self, message):
        self.detail = message
