from django.urls import include,path

urlpatterns = [
    path('accounts/v1/', include('accounts.urls')),
]