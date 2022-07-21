from .models import Marker
from rest_framework import viewsets
from .serializers import MarkerSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class MarkerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Marker.objects.all()
    serializer_class = MarkerSerializer
