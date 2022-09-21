from .models import Marker, Reward, Tag, Clear

from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from rest_framework import viewsets, generics
from .serializers import MarkerSerializer, MarkerSimpleSerializer, RewardSerializer, TagSerializer, \
    MarkerImageSerializer, ClearSerializer, ClearListSerializer, LogSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q


class MarkerViewSet(viewsets.ModelViewSet):
    queryset = Marker.objects.all()
    serializer_class = MarkerSerializer

    def perform_create(self, serializer):
        serializer.save(status="U", posted_user=self.request.user)

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

        return Response({"status": "success"}, status=status.HTTP_200_OK)


class MarkerSimpleViewSet(viewsets.ModelViewSet):
    queryset = Marker.objects.filter(Q(status="U") | Q(status="W"))
    serializer_class = MarkerSimpleSerializer


class RewardViewSet(viewsets.ModelViewSet):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer

    def perform_create(self, serializer):
        serializer.save(status="W", helper=self.request.user)


class MypageViewSet(viewsets.ModelViewSet):
    serializer_class = LogSerializer

    def get_queryset(self):
        user = self.request.user
        clears = Clear.objects.filter(Q(cleanup_user=user) & Q(status="C"))

        return clears


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ClearViewSet(viewsets.ModelViewSet):
    queryset = Clear.objects.all()
    serializer_class = ClearSerializer

    def perform_create(self, serializer):
        serializer.save(cleanup_user=self.request.user, marker_id=self.request.data['marker'])


class ChargePointAPI(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        user.point += 1000
        user.save()
        return Response(status=status.HTTP_200_OK)


@permission_classes([AllowAny])
class VerifyPaymentsAPI(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        return Response({"success": "true"}, status=status.HTTP_200_OK)


class MarkerWaitingViewSet(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        clears = Clear.objects.filter(
            Q(marker__posted_user=request.user) & Q(status="W")
        )
        serializer = ClearListSerializer(clears, many=True)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        clear_id = request.data['clear_id']
        clear = Clear.objects.get(id=clear_id)

        clear_status = request.data['status']
        if clear_status == 'approve':
            clear.status = "C"
            clear.marker.status = "C"
            clear.marker.cleanup_user = clear.cleanup_user
            clear.marker.save()
            clear.cleanup_user.point += int(clear.marker.reward.reward * 0.9)
            clear.cleanup_user.save()
            clear.save()

        elif clear_status == 'reject':
            clear.marker.status = "W"
            clear.status = "D"
            clear.save()

        return Response(status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        clear = Clear.objects.get(id=pk)
        serializer = ClearSerializer(clear)
        return Response(serializer.data, status=status.HTTP_200_OK)
