"""该包中含有所有加密和解密的相关方法"""
import base64
import hashlib
import json
import re

ALL_CHARS = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
PREFIX = '32hj21ju-aw31-34c3-ad1v-da3d3d23ij09'
AUTO_ADD_NUM = 234565432


def is_valid_short_code(func):

    def wrapper(*args, **kwargs):
        args = (re.sub(r'[^\w]', '', args[0]), )
        return func(*args, **kwargs)
    return wrapper


def password_encode(password: str, prefix=PREFIX) -> str:
    """密码加密"""
    h = hashlib.sha256()
    h.update((prefix+password).encode('utf-8'))
    return h.hexdigest()


def short_char_encode(num: int) -> str:
    """制造短链"""
    num += AUTO_ADD_NUM
    digits = []
    while num > 0:
        digits.append(ALL_CHARS[num % 62])
        num //= 62
    return ''.join(digits[::-1])


@is_valid_short_code
def short_char_decode(short_code: str) -> int:
    """短链还原"""
    print(short_code)
    num = 0
    lens = len(short_code)
    for idx, val in enumerate(short_code):
        num += ALL_CHARS.find(val) * 62 ** (lens-1-idx)
    num -= AUTO_ADD_NUM
    return num


def obj_encode(encode_str):
    if not isinstance(encode_str, bytes):
        encode_str = encode_str.encode('utf-8')
    return base64.b64encode(encode_str)


def obj_decode(decode_str):
    if not isinstance(decode_str, bytes):
        decode_str = decode_str.encode('utf-8')
    return base64.b64decode(decode_str)

# a = obj_encode(json.dumps(["高新区","gaoxin7"])).decode('utf-8')
# b = obj_decode(a)
# c = json.loads(b.decode('utf-8'))
# d = json.loads(obj_decode(a).decode('utf-8'))
# print(a, type(a))
# print(b)
# print(c, type(c))
# print(d, type(d))
