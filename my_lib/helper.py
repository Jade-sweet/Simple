import datetime
import uuid

from rest_framework.response import Response

from api.v1.user.models import Token


class DefaultResponse(Response):

    def __init__(self, code=1000, message='操作成功',
                 data=None, status=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None):
        _data = {'code': code, 'message': message}
        if data:
            _data.update(data)
        super().__init__(_data, status, template_name, headers, exception, content_type)


def auto_add_token(num: int) -> str:
    """自动向表中添加token并返回该key"""
    token_id = str(uuid.uuid4())
    t = Token()
    t.tid = token_id
    t.uid = num
    now_time = datetime.datetime.now()
    later_time = datetime.timedelta(seconds=60*60)  # 登录一小时后自动过期
    t.expire_time = now_time + later_time
    t.save()
    return token_id
