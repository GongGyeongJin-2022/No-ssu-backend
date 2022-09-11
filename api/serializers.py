from dataclasses import field
from rest_framework import serializers
from .models import Marker, Reward
from accounts.models import User


class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = '__all__'


class MarkerSerializer(serializers.ModelSerializer):

    reward = RewardSerializer(many=False)

    posted_user = serializers.ReadOnlyField

    class Meta:
        model = Marker
        fields = '__all__'

    def create(self, validated_data):
        reward_data = validated_data.pop('reward')
        reward = Reward.objects.create(**reward_data)
        tags = validated_data.pop('tags')
        marker = Marker.objects.create(reward=reward, **validated_data)

        for tag in tags:
            marker.tags.add(tag)
        return marker
  
    


class MarkerSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Marker
        fields = ("longitude","latitude","reward")


class ProfileSerializer(serializers.ModelSerializer):

    reward = RewardSerializer(many=False)

    class Meta:
        model = Marker
        fields = ("longitude","latitude","reward")

class ChargePointSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id','point')

    def update(self, instance, validated_data):

        instance.point += validated_data.get('point', instance.point)
        instance.save()

        return instance



    