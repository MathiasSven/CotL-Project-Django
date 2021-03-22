from rest_framework import serializers
from .models import *


class AllianceMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllianceMember
        fields = '__all__'


class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = '__all__'


class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = '__all__'