from django.urls import path
from apps.account.apis.auth.password.verify import TokenVerifyAPIView
from apps.account.apis.custom_user import CustomUserListCreateAPIView, CustomUserDetaileAPIView


urlpatterns = [
    path('users/', CustomUserListCreateAPIView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', CustomUserDetaileAPIView.as_view(), name='user-detail'),
    path('auth/token/verify/', TokenVerifyAPIView.as_view(), name='token_verify'),
]
