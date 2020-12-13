from abc import ABC

from rest_framework import serializers

from api.v1.user.models import User
from my_lib.re_helper import check_name, ParamsException, check_nick_name, check_password


class SimpleSerializer(serializers.ModelSerializer):
    """简单序列化器"""
    class Meta:
        model = User
        fields = ('id', 'name',)


class DetailSerializer(serializers.ModelSerializer):
    """详细的序列化器"""

    class Meta:
        model = User
        # 显示所有字段
        exclude = ('is_deleted', )


class CreateSerializer(serializers.ModelSerializer):
    """新建序列化器"""
    password = serializers.SerializerMethodField()

    @staticmethod
    def get_password():
        pass

    class Meta:
        model = User
        # 显示所有字段
        fields = '__all__'


class RegisterSerializer(serializers.Serializer):
    """注册验证序列化类"""
    name = serializers.CharField(required=True, error_messages={'required': '用户名不能为空'})
    nick_name = serializers.CharField(required=True, error_messages={'required': '昵称不能为空'})
    password = serializers.CharField(required=True, error_messages={'required': '密码不能为空'})

    def validate(self, attrs):
        """实际验证"""
        name = attrs.get('name')
        nick_name = attrs.get('nick_name')
        password = attrs.get('password')
        if not check_name(name):
            raise ParamsException({'code': 4001, 'message': '用户名不符合规范'})
        if User.objects.filter(name=name).exists():
            raise ParamsException({'code': 4002, 'message': '用户名已存在'})
        if not check_nick_name(nick_name):
            raise ParamsException({'code': 4003, 'message': '昵称不符合规范'})
        if not check_password(password):
            raise ParamsException({'code': 4004, 'message': '密码不符合规范'})
        return attrs


class LoginSerializer(serializers.Serializer):
    """登录验证序列化类"""
    name = serializers.CharField(required=True, error_messages={'required': '用户名不能为空'})
    password = serializers.CharField(required=True, error_messages={'required': '密码不能为空'})

    def validate(self, attrs):
        """实际验证"""
        name = attrs.get('name')
        password = attrs.get('password')
        if not check_name(name):
            raise ParamsException({'code':5001, 'message': '用户名不符合规范'})
        if not User.objects.filter(name=name).exists():
            raise ParamsException({'code': 5002, 'message': '用户名输入错误'})
        if not check_password(password):
            raise ParamsException({'code': 5003, 'message': '密码输入错误'})
        return attrs
