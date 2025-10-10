# yourapp/urls.py
from django.urls import path
from utility.otpcode.logout import LogoutView
from utility.otpcode.otp_api import RequestOTPAPIView
from utility.otpcode.test_auth import TestAuthAPIView
from utility.otpcode.verify_otp import VerifyOTPAPIView
from utility.otpcode.refresh_api import RefreshTokenAPIView


urlpatterns = [
    path("request-otp", RequestOTPAPIView.as_view(), name="request_otp"),
    path("verify-otp", VerifyOTPAPIView.as_view(), name="verify_otp"),
    path("test-auth", TestAuthAPIView.as_view(), name="test_auth"),  
    path("refresh-token", RefreshTokenAPIView.as_view(), name="refresh_token"),
    path("logout",LogoutView.as_view(), name="logout"),

]