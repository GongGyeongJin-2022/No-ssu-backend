from .models import Marker, Reward, Tag
from accounts.models import User
from rest_framework import viewsets, generics
from .serializers import MarkerSerializer, MarkerSimpleSerializer, RewardSerializer, ProfileSerializer, TagSerializer, \
    MarkerImageSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from datetime import datetime

from .utils import send_push_message


class MarkerViewSet(viewsets.ModelViewSet):
    queryset = Marker.objects.all()
    serializer_class = MarkerSerializer

    def perform_create(self, serializer):
        serializer.save(posted_user=self.request.user)

    def perform_destroy(self, request, pk=None):
        marker_id = self.kwargs['pk']
        marker = Marker.objects.get(id=marker_id)
        reward = marker.reward
        user = self.request.user

        marker.cleanup_user = user
        marker.status = 'C'
        user.point += reward.reward

        marker.save()
        user.save()

        # 마커 올린 시간
        posted_time = marker.posted_time
        send_push_message(marker.posted_user, {'title': '마커 처리 알림', 'body': f'{posted_time.hour}시 {posted_time.minute}분에 올린 마커가 처리되었습니다.'})

        return Response({"status": "success"}, status=status.HTTP_200_OK)


class MarkerSimpleViewSet(viewsets.ModelViewSet):
    queryset = Marker.objects.all()
    serializer_class = MarkerSimpleSerializer


class RewardViewSet(viewsets.ModelViewSet):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer

    def perform_create(self, serializer):
        serializer.save(helper=self.request.user)


class MypageViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        user = self.request.user
        marker = Marker.objects.all()
        return marker.filter(Q(posted_user=user) | Q(cleanup_user=user))


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ChargePointView(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        current_user = self.request.user.id
        print(1)
        user = User.objects.get(id=current_user)
        print(2)
        user.point += int(self.request.data.get('point'))
        print(3)
        user.save()
        return Response({'detail': 'Success'})
