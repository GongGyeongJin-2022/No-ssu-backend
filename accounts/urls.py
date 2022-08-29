from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('', include('allauth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('login/google/finish/', views.GoogleLogin.as_view(), name='google_login_finish'),
    path('login/google/', views.google_login, name='google_login'),
    path('login/google/callback/', views.google_callback, name='google_callback'),
]