from django.shortcuts import render
from .models import Marker

def home(request):
    markers = Marker.objects
    return render(request,'')
