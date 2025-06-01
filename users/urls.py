from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserRegisterView,
    MyTokenObtainPairView,
    UserProfileView,
    PasswordResetView,
    PasswordResetConfirmView,
)

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('reset_password/', PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_confirm/', PasswordResetConfirmView.as_view(), name='reset_password_confirm'),
]