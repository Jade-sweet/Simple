from django.db.models import Q
from django.db.transaction import atomic
from django.shortcuts import render

# Create your views here.
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view

from api.v1.serializers.user import RegisterSerializer, LoginSerializer
from api.v1.user.models import User
from my_lib.code_encryption import short_char_encode, password_encode
from my_lib.helper import DefaultResponse, auto_add_token


@swagger_auto_schema(
    method='post',
    operation_summary='[可用]根据用户输入来新建用户',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['name', 'nick_name', 'password'],
        property={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='用户名 example: 龙泉驿区'),
            'nick_name': openapi.Schema(type=openapi.TYPE_STRING, description='昵称 example: 龙泉驿区'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='密码 example: 龙泉驿区')
        }
    ),
    security=[]

)
@api_view(('POST', ))
def register(request):
    """用户注册"""
    data = request.data
    serializer = RegisterSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    with atomic():
        user = User()
        user.name = serializer.validated_data['name']
        user.nick_name = serializer.validated_data['nick_name']
        user.password = password_encode(serializer.validated_data['password'])
        user.save()
    return DefaultResponse(200, '注册成功',{'results': {'nick_name': serializer.validated_data['nick_name']}})


@swagger_auto_schema(
    method='post',
    operation_summary='[可用]根据用户输入登录，返回登录凭证',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['name', 'password'],
        property={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='用户名 example: ghjsdadds'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='密码 example: 345678Ad.')
        }
    ),
    security=[]
)
@api_view(('POST', ))
def login(request):
    """用户登录"""
    data = request.data
    serializer = LoginSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    name = serializer.validated_data['name']
    password = password_encode(serializer.validated_data['password'])
    user = User.objects.filter(Q(name=name) & Q(password=password)).first()
    if user:
        # 设置token，返回tid
        tid = auto_add_token(user.id)
        return DefaultResponse(200, '登录成功', {'results': {'token': tid}})
    return DefaultResponse(200, '登录失败')
