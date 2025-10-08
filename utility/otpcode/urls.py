# yourapp/urls.py
from django.urls import path
from utility.otpcode.otp_api import RequestOTPAPIView
from utility.otpcode.test_auth import TestAuthAPIView
from utility.otpcode.verify_otp import VerifyOTPAPIView


urlpatterns = [
    path("request-otp", RequestOTPAPIView.as_view(), name="request_otp"),
    path("verify-otp", VerifyOTPAPIView.as_view(), name="verify_otp"),
    path("test-auth", TestAuthAPIView.as_view(), name="test_auth"),  # 🔥 endpoint تست
]