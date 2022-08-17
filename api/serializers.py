from rest_framework import serializers
from .models import Marker, Reward


class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = '__all__'


class MarkerSerializer(serializers.ModelSerializer):

    reward = RewardSerializer()

    class Meta:
        model = Marker
        fields = '__all__'