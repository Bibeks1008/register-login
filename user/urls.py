from django.urls import path, include

from user.views.auth import RegisterUserAPIView, LoginAPIView, PasswordResetAPIView

app_name = 'user'

urlpatterns=[
    path('api/register/', RegisterUserAPIView.as_view(), name='user_registration'),
    path('api/login/', LoginAPIView.as_view(), name='user_login'),
    path('api/password-reset/', PasswordResetAPIView.as_view(), name='reset-password'),
]