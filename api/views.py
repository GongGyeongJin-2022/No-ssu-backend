from django.shortcuts import render
from .models import Marker
from rest_framework import viewsets
from .serializers import MarkerSerializer

class MarkerViewSet(viewsets.ModelViewSet):
    queryset = Marker.objects.all()
    serializer_class = MarkerSerializer
