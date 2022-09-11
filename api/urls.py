from django.urls import include,path
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()

router.register('marker', views.MarkerViewSet)
router.register('reward', views.RewardViewSet)
router.register('simple', views.MarkerSimpleViewSet, basename='simple')
router.register('mypage', views.MypageViewSet, basename= 'mypage')
# router.register('charge-point', views.ChargePointViewSet, basename= 'charge-point')



urlpatterns = [
    path('', include(router.urls)),
    path('accounts/v1/', include('accounts.urls')),
    path('charge-point/', views.ChargePointView.as_view())
]

