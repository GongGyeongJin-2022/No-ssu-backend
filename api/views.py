from ctypes import pointer
from .models import Marker, Reward
from accounts.models import User
from rest_framework import viewsets
from .serializers import ChargePointSerializer, MarkerSerializer, MarkerSimpleSerializer, RewardSerializer, ProfileSerializer
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(gave_user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class MypageViewSet(viewsets.ModelViewSet):

    serializer_class = ProfileSerializer

    def get_queryset(self):
        user = self.request.user
        marker = Marker.objects.all()
        return marker.filter(Q(posted_user = user) | Q(cleanup_user = user))



class ChargePointViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ChargePointSerializer

    def get_queryset(self):
        current_user = self.request.user.id
        user = User.objects.all()
        return user.filter(id=current_user)

    def create(self, request, *args, **kwargs):
        instance = self.get_queryset().get(id=self.request.user.id)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)





    


