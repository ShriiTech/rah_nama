from django.urls import path

from account.apis.phone_token import PhoneTokenObtainView
from account.apis.auth.password.verify import TokenVerifyAPIView
from account.apis.custom_user import CustomUserListCreateAPIView, CustomUserDetaileAPIView

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


urlpatterns = [
    path('users', CustomUserListCreateAPIView.as_view(), name='user_list_create'),
    path('users/<int:pk>', CustomUserDetaileAPIView.as_view(), name='user_detail'),
    path('auth/token/verify', TokenVerifyAPIView.as_view(), name='token_verify'),
    path('login-by-phone', PhoneTokenObtainView.as_view(), name='token_by_phone'),
    path('api/schema', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger_ui'),
    path('api/redoc', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
