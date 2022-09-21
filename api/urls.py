from django.urls import include,path
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()

router.register('marker', views.MarkerViewSet)
router.register('reward', views.RewardViewSet)
router.register('simple', views.MarkerSimpleViewSet, basename='simple')
router.register('mypage', views.MypageViewSet, basename='mypage')
router.register('tag', views.TagViewSet, basename='tag')
router.register('clear', views.ClearViewSet, basename='clear')
router.register('marker-waiting', views.MarkerWaitingViewSet, basename='marker-waiting')


urlpatterns = [
    path('accounts/v1/', include('accounts.urls')),
    path('charge-point/', views.ChargePointAPI.as_view()),
    path('verify-payments/', views.VerifyPaymentsAPI.as_view()),
    path('', include(router.urls)),
]

