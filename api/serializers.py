from rest_framework import serializers
from .models import Marker, Reward


class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = '__all__'


class MarkerSerializer(serializers.ModelSerializer):
    reward = RewardSerializer(many=False)

    class Meta:
        model = Marker
        fields = ('longitude', 'latitude', 'image', 'explanation', 'tags', 'size', 'reward')
