from django.urls import path
from account.apis.auth.password.verify import TokenVerifyAPIView
from account.apis.custom_user import CustomUserListCreateAPIView, CustomUserDetaileAPIView
from account.apis.phone_token_obtain import PhoneTokenObtainView


urlpatterns = [
    path('users', CustomUserListCreateAPIView.as_view(), name='user_list_create'),
    path('users/<int:pk>', CustomUserDetaileAPIView.as_view(), name='user_detail'),
    path('auth/token/verify', TokenVerifyAPIView.as_view(), name='token_verify'),
    path('login-by-phone', PhoneTokenObtainView.as_view(), name='token_by_phone'),

]
