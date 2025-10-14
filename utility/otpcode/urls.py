from django.urls import path
from utility.otpcode.logout import LogoutView
from utility.otpcode.otp_api import RequestOTPAPIView
from account.apis.auth.jwt.is_authenticated_apis import IsAuthenticatedAPIView
from utility.otpcode.verify_otp import VerifyOTPAPIView
from account.apis.auth.jwt.refresh_api import RefreshTokenAPIView


urlpatterns = [
    path("request-otp", RequestOTPAPIView.as_view(), name="request_otp"),
    path("verify-otp", VerifyOTPAPIView.as_view(), name="verify_otp"),
    path("test-auth", IsAuthenticatedAPIView.as_view(), name="test_auth"),  
    path("refresh-token", RefreshTokenAPIView.as_view(), name="refresh_token"),
    path("logout",LogoutView.as_view(), name="logout"),
]
