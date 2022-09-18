from ctypes import pointer

from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from .models import Marker, Reward, Tag
from accounts.models import User
from rest_framework import viewsets, generics
from .serializers import MarkerSerializer, MarkerSimpleSerializer, RewardSerializer, ProfileSerializer, TagSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.shortcuts import get_object_or_404


class MarkerViewSet(viewsets.ModelViewSet):
    queryset = Marker.objects.all()
    serializer_class = MarkerSerializer

    def perform_create(self, serializer):
        serializer.save(posted_user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        marker_id = self.kwargs['pk']
        print(self.kwargs)
        marker = Marker.objects.get(id=marker_id)
        reward = marker.reward
        user = request.user

        marker.cleanup_user = user
        marker.status = 'C'
        user.point += reward.reward

        marker.save()
        user.save()

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


@permission_classes([AllowAny])
class ChargePointView(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        print(request.data)
        # current_user = self.request.user.id
        # print(1)
        # user = User.objects.get(id=current_user)
        # print(2)
        # user.point += int(self.request.data.get('point'))
        # print(3)
        # user.save()
        return Response({"success": True}, status=status.HTTP_200_OK)
