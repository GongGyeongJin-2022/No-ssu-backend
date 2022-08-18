from django.urls import include,path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register('marker', views.MarkerViewSet)
router.register('reward', views.RewardViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('accounts/v1/', include('accounts.urls')),
]
