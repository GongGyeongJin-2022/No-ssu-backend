from .models import Marker
from rest_framework import viewsets
from .serializers import MarkerSerializer,RewardSerializer

class MarkerViewSet(viewsets.ModelViewSet):
    queryset = Marker.objects.all()
    serializer_class = MarkerSerializer

class RewardViewSet(viewsets.ModelViewSet):
    queryset = Marker.objects.all()
    serializer_class = RewardSerializer

