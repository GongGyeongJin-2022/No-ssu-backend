from dataclasses import field
from rest_framework import serializers
from .models import Marker, Reward


class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = '__all__'


class MarkerSerializer(serializers.ModelSerializer):

    posted_user = serializers.ReadOnlyField

    reward = RewardSerializer(many=False, read_only=True)
    reward_reward = serializers.IntegerField(write_only=True)

    class Meta:
        model = Marker
        fields = ('id','reward','longitude','latitude','image','explanation','size','posted_time','status','posted_user','cleanup_user','tags','reward_reward')
        extra_kwargs = {
            'reward_reward': {'write_only': True},
        }

    def create(self, validated_data):
        reward_data = validated_data.pop('reward_reward', None)
        print(reward_data)
        reward = Reward.objects.create(reward=reward_data, gave_user=validated_data["posted_user"])
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


    