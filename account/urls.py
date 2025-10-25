from django.urls import path, include

from account.apis import PersonalInfoAPIView, PasswordLoginAPIView
from account.apis.models import CustomUserListAPIView, CustomUserDetailAPIView
from account.apis.auth.jwt import IsAuthenticatedAPIView, LogoutView, RefreshTokenAPIView
from account.apis.auth.jwt.otp import RequestOTPAPIView, VerifyOTPAPIView
from account.apis.update.email import RequestEmailChangeView, VerifyEmailChangeView


urlpatterns = [
    path('users', CustomUserListAPIView.as_view(), name='user_list'),
    path('users/<int:pk>', CustomUserDetailAPIView.as_view(), name='user_detail'),
    path('auth/', include([
        path('jwt/', include([
            path('otp/', include([
                path('request', RequestOTPAPIView.as_view(), name="request_otp"),
                path("verify", VerifyOTPAPIView.as_view(), name="verify_otp"),
            ])),
            path('password-login', PasswordLoginAPIView.as_view(), name='token_by_phone'),
            path("refresh-token", RefreshTokenAPIView.as_view(), name="refresh_token"),
            path("logout", LogoutView.as_view(), name="logout"),
        ])),
        path("auth-check", IsAuthenticatedAPIView.as_view(), name="test_auth"),  
    ])),
    path('personal-info', PersonalInfoAPIView.as_view(), name='me'),
    path('update/', include([
        path('email/', include([
            path("request", RequestEmailChangeView.as_view(), name="update-email-request"),
            path("verify", VerifyEmailChangeView.as_view(), name="update-email-verify"),
        ])),
    ])),
]
