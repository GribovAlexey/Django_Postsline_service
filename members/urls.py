from .views import UserRegisterView
from django.urls import path, include

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', UserRegisterView.as_view(), name='register'),
]
