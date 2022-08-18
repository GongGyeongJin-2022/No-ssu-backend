from .models import Marker, Reward
from accounts.models import User
from rest_framework import viewsets
from .serializers import MarkerSerializer,RewardSerializer
from rest_framework.response import Response
from rest_framework import status


class MarkerViewSet(viewsets.ModelViewSet):
    queryset = Marker.objects.all()
    serializer_class = MarkerSerializer

    def destroy(self, request, *args, **kwargs):
        marker_id = self.kwargs['pk']
        print(self.kwargs)
        marker = Marker.objects.get(id=marker_id)
        reward = marker.reward
        user = request.user
        
        marker.cleanup_user = user
        # 마커 상태 waiting에서 cleaned로 바뀌고
        marker.status = 'C'
        # marker.reward만큼 user.point 증가 (올린 사람이 치운 사람한테?)
        user.point += reward.reward

        marker.save()
        user.save()

        return Response({"data": "success"}, status=status.HTTP_200_OK)



class RewardViewSet(viewsets.ModelViewSet):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer

            




