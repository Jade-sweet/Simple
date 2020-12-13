import datetime
import uuid

from django.db.models import Q
from django_filters import filterset
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from api.v1.crawler.models import HouseInfo
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


class CustomPagePagination(PageNumberPagination):
    """自定义页码分页类"""
    page_size_query_param = 'size'
    max_page_size = 50


class HouseInfoFilter(filterset.FilterSet):
    """房屋过滤类"""
    min_price = filterset.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filterset.NumberFilter(field_name='price', lookup_expr='lte')
    area = filterset.CharFilter(method='filter_by_area')

    @staticmethod
    def filter_by_area(queryset, name, value):
        return queryset.filter(Q(county__startswith=value) |
                               Q(street__startswith=value) |
                               Q(xiaoqu__startswith=value))

    class Meta:
        model = HouseInfo
        fields = ('min_price', 'max_price', 'county')
