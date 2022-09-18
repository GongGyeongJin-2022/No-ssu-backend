from dataclasses import field
from rest_framework import serializers
from .models import Marker, Reward, Tag, MarkerImage
from accounts.models import User


class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = '__all__'

class MarkerImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarkerImage
        fields = ['image', 'marker']

class MarkerSerializer(serializers.ModelSerializer):

    posted_user = serializers.ReadOnlyField

    reward = RewardSerializer(many=False, read_only=True)
    images = MarkerImageSerializer(source='markerimage_set', many=True, read_only=True)
    reward_reward = serializers.IntegerField(write_only=True)
    # images_image = serializers.FileField(write_only=True)

    class Meta:
        model = Marker
        fields = ('id','reward','longitude','latitude','explanation','size','posted_time','status','posted_user','cleanup_user','tags','reward_reward','images')
        extra_kwargs = {
            'reward_reward': {'write_only': True}
        }

    def create(self, validated_data):
        reward_data = validated_data.pop('reward_reward', None)
        reward = Reward.objects.create(reward=reward_data, gave_user=validated_data["posted_user"])
        tags = validated_data.pop('tags')
        images = self.context.get('view').request.FILES
        marker = Marker.objects.create(reward=reward, **validated_data)

        for image in images.values():
            MarkerImage.objects.create(marker=marker, image=image)

        for tag in tags:
            marker.tags.add(tag)
        return marker

  
    


class MarkerSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Marker
        fields = ("id","longitude","latitude","reward")


class ProfileSerializer(serializers.ModelSerializer):

    reward = RewardSerializer(many=False)

    class Meta:
        model = Marker
        fields = ("longitude","latitude","reward")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

# class ChargePointSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = User
#         fields = ('id','point')
#
#     def update(self, instance, validated_data):
#
#         instance.point += validated_data.get('point', instance.point)
#         instance.save()
#
#         return instance



    