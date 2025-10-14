from django.urls import path, include

from account.apis.auth.jwt.is_authenticated_apis import IsAuthenticatedAPIView
from account.apis.auth.jwt.logout_apis import LogoutView
from account.apis.auth.jwt.otp.request_apis import RequestOTPAPIView
from account.apis.auth.jwt.otp.verify_apis import VerifyOTPAPIView
from account.apis.phone_token import PhoneTokenObtainView
from account.apis.auth.password.verify import TokenVerifyAPIView
from account.apis.models.custom_user_apis import CustomUserListCreateAPIView, CustomUserDetaileAPIView
from account.apis.my.my_custom_user import MyCustomUserAPIView
from account.apis.phone_token import PhoneTokenObtainView
from account.apis.auth.jwt.refresh_api import RefreshTokenAPIView


urlpatterns = [
    path('users', CustomUserListCreateAPIView.as_view(), name='user_list_create'),
    path('users/<int:pk>', CustomUserDetaileAPIView.as_view(), name='user_detail'),
    path('auth/', include(
        path('request-otp', RequestOTPAPIView.as_view(), name="request_otp"),
        path('', TokenVerifyAPIView.as_view(), name='token_verify'),

        path("verify-otp", VerifyOTPAPIView.as_view(), name="verify_otp"),
        path("test-auth", IsAuthenticatedAPIView.as_view(), name="test_auth"),  
        path("refresh-token", RefreshTokenAPIView.as_view(), name="refresh_token"),
        path("logout",LogoutView.as_view(), name="logout"),
    )),
    path('login-by-phone', PhoneTokenObtainView.as_view(), name='token_by_phone'),

    path('me', MyCustomUserAPIView.as_view(), name='me'),
]
