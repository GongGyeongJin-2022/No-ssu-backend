from dataclasses import field
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField, CharField, DecimalField, IntegerField

from No_ssu_backend import settings
from rest_framework.relations import PrimaryKeyRelatedField

from .models import Marker, Reward, Tag, MarkerImage, Clear, ClearImage
from accounts.models import User
from accounts.serializers import UserSerializer
from .utils import send_push_message


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
    images = SerializerMethodField(read_only=True)
    reward_reward = serializers.IntegerField(write_only=True)

    # images_image = serializers.FileField(write_only=True)

    class Meta:
        model = Marker
        fields = (
            'id', 'reward', 'longitude', 'latitude', 'explanation', 'size', 'posted_time', 'status', 'posted_user',
            'tags',
            'reward_reward', 'images')
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

    def get_images(self, instance):
        return [settings.MEDIA_URL + str(item.image) for item in instance.images.all()]


class MarkerSimpleSerializer(serializers.ModelSerializer):
    reward = IntegerField(source='reward.reward', read_only=True)

    class Meta:
        model = Marker
        fields = ("id", "longitude", "latitude", "reward", "status")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ClearSerializer(serializers.ModelSerializer):
    cleanup_user = PrimaryKeyRelatedField(read_only=True)
    status = CharField(read_only=True)
    images = SerializerMethodField(read_only=True)

    class Meta:
        model = Clear
        fields = ('marker', 'cleanup_user', 'status', 'explanation', 'images')
        depth = 2

    def create(self, validated_data):
        print(validated_data)
        images = self.context.get('view').request.FILES
        clear = Clear.objects.create(**validated_data)
        marker = Marker.objects.get(id=validated_data['marker_id'])
        marker.status = "W"
        marker.save()

        for image in images.values():
            ClearImage.objects.create(clear=clear, image=image)

        # 마커 올린 시간
        posted_time = marker.posted_time
        send_push_message(marker.posted_user,
                          {'title': '마커 처리 알림', 'body': f'{posted_time.hour}시 {posted_time.minute}분에 올린 마커가 처리되었습니다.'})

        return clear

    def get_images(self, instance):
        return [settings.MEDIA_URL + str(item.image) for item in instance.images.all()]


class LogSerializer(serializers.ModelSerializer):
    latitude = DecimalField(source='marker.latitude', max_digits=20, decimal_places=14, read_only=True)
    longitude = DecimalField(source='marker.longitude', max_digits=20, decimal_places=14, read_only=True)
    posted_user = CharField(source='marker.posted_user.first_name', read_only=True)
    cleanup_user = CharField(source='cleanup_user.first_name', read_only=True)
    reward = IntegerField(source='marker.reward.reward', read_only=True)

    class Meta:
        model = Clear
        fields = ("latitude", "longitude", "posted_user", "cleanup_user", "created_at", "reward")


class ClearListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clear
        fields = ("id",)
