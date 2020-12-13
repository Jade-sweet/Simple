from rest_framework import serializers

from api.v1.crawler.models import HouseInfo
from my_lib.re_helper import ParamsException

VALID_HOUSE_TYPES = ['二手房', '新房']
VALID_AREA = ['龙泉驿区', '锦江区', '高新区']
AREA_DICT = {
    '龙泉驿区': ['龙泉驿区', 'longquanyi'],
    '锦江区': ['锦江区','jinjiang'],
    '高新区': ['高新区','gaoxin7']
}


class SimpleSerializer(serializers.Serializer):
    house_type = serializers.CharField(required=True, error_messages={'required': '房源类型不允许为空'})
    area = serializers.CharField(required=True, error_messages={'required': '地区不允许为空'})

    def validate(self, attrs):
        house_type = attrs.get('house_type')
        area = attrs.get('area')
        if house_type not in VALID_HOUSE_TYPES:
            raise ParamsException({'code': 5001, 'message': f'指定房屋类型错误，目前只支持 {VALID_HOUSE_TYPES}'})
        if area not in VALID_AREA:
            raise ParamsException({'code': 5001, 'message': f'指定地区类型错误，目前只支持 {VALID_AREA}'})
        return attrs


class SearchSerializer(serializers.Serializer):
    county = serializers.CharField(required=True, error_messages={'required': '区不允许为空'})
    min_price = serializers.IntegerField(required=True, error_messages={'required': '最小价格不允许为空'})
    max_price = serializers.IntegerField(required=True, error_messages={'required': '最大价格不允许为空'})

    def validate(self, attrs):
        min_price = attrs.get('min_price')
        max_price = attrs.get('max_price')
        if min_price > max_price:
            raise ParamsException({'code': 5003, 'message': f'最小值应该小于等于最大值'})
        return attrs


class SearchResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = HouseInfo
        exclude = ('house_id', )