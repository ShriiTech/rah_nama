from django.urls import path
from account.apis.auth.jwt.logout_apis import LogoutView
from account.apis.auth.jwt.otp.request_apis import RequestOTPAPIView
from account.apis.auth.jwt.otp.verify_apis import VerifyOTPAPIView
from account.apis.auth.jwt.is_authenticated_apis import IsAuthenticatedAPIView
from account.apis.auth.jwt.refresh_api import RefreshTokenAPIView


urlpatterns = [
    path("request-otp", RequestOTPAPIView.as_view(), name="request_otp"),
    path("verify-otp", VerifyOTPAPIView.as_view(), name="verify_otp"),
    path("test-auth", IsAuthenticatedAPIView.as_view(), name="test_auth"),  
    path("refresh-token", RefreshTokenAPIView.as_view(), name="refresh_token"),
    path("logout",LogoutView.as_view(), name="logout"),
]
