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
        fields = '__all__'

    def create(self, validated_data):
        reward_data = validated_data.pop('reward')
        reward = Reward.objects.create(**reward_data)
        tags = validated_data.pop('tags')
        print(tags)
        marker = Marker.objects.create(reward=reward, **validated_data)

        for tag in tags:
            marker.tags.add(tag)
        return marker
