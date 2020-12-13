import datetime
import json

from django.db.models import Q

# Create your views here.
from drf_yasg import openapi
from drf_yasg.openapi import Parameter, IN_PATH, IN_QUERY, TYPE_INTEGER, TYPE_STRING
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import BaseAuthentication
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.exceptions import AuthenticationFailed

from api.v1.crawler.models import HouseInfo
from api.v1.serializers.crawler import SimpleSerializer, SearchSerializer, AREA_DICT, SearchResultSerializer
from api.v1.user.models import Token
from my_lib.code_encryption import obj_encode
from my_lib.helper import DefaultResponse
from my_lib.tasks import Task, TaskQueue


class SignInAuthentication(BaseAuthentication):
    """权限验证"""
    def authenticate(self, request):
        token = request.data.get('HTTP_TOKEN')
        if token:
            """鉴定合法性  由于存放在sqlite中，则取最后一条登录记录， 即用户多次登录，只有最后一次有效"""
            instance = Token.objects.filter(tid=token).first()
            if instance:
                """取出对应的uid的未过期的值，按有效期从大到小排序"""
                valid_instances = Token.objects.filter(Q(uid=instance.uid) & Q(is_expire=False) & Q(expire_time__gt=datetime.datetime.now())).order_by('-expire_time')
                if valid_instances and valid_instances[0].tid == token:
                    return instance, token
        raise AuthenticationFailed({'code': 401, 'message': '尚未登录或登录超时，请重新登录'})


@swagger_auto_schema(
    method='post',
    operation_summary='[可用]用于启动爬虫',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['county', 'house_type'],
        property={
            'county': openapi.Schema(type=openapi.TYPE_STRING, description='指定地区 example: 龙泉驿区'),
            'house_type': openapi.Schema(type=openapi.TYPE_STRING, description='指定类型 example: 二手房'),
            'HTTP_TOKEN': openapi.Schema(type=openapi.TYPE_STRING, description='认证凭据'),
        }
    )
)
@api_view(('POST',))
@authentication_classes((SignInAuthentication, ))
def add_new(request):
    """新增爬虫"""
    data = request.data
    print(data, 111)
    serializer = SimpleSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    house_type = serializer.validated_data['house_type']
    area = serializer.validated_data['area']
    new_task = Task(house_type=house_type, area=obj_encode(json.dumps(AREA_DICT[area])).decode('utf-8'))
    TaskQueue().push(new_task)  # 添加任务
    return DefaultResponse(200, '爬虫成功启动', {'results': {'type': house_type, 'area': area}})


@swagger_auto_schema(
    method='get',
    operation_summary='[可用]用于查询爬取的数据',
    manual_parameters=[
        Parameter(name='county', in_=IN_QUERY, description='房屋所在区', type=TYPE_STRING, required=True),
        Parameter(name='HTTP_TOKEN', in_=IN_PATH, description='认证凭据', type=TYPE_STRING, required=True),
        Parameter(name='min_price', in_=IN_QUERY, description='最低价格', type=TYPE_INTEGER, required=False),
        Parameter(name='max_price', in_=IN_QUERY, description='最高价格', required=False, type=TYPE_INTEGER),
],
    security=[]
)
@api_view(('GET',))
@authentication_classes((SignInAuthentication, ))
def search(request):
    """查找信息"""
    data = request.query_params
    print(data)
    serializer = SearchSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    county = serializer.validated_data['county']
    min_price = serializer.validated_data['min_price']
    max_price = serializer.validated_data['max_price']
    # 查找逻辑
    queryset = HouseInfo.objects.filter(Q(county__startswith=county) & Q(price__gte=min_price) & Q(price__lte=max_price)).all().order_by('area')
    count = queryset.count()
    # 结果集序列化器
    serializer = SearchResultSerializer(queryset, many=True)
    return DefaultResponse(200, '成功查询', {'results': {'count': count, 'data': serializer.data}})


