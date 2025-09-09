from datetime import timedelta

REST_FRAMEWORK = {
    # 🔑 Authentication
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),

    # 🔐 Permission: به صورت پیش‌فرض فقط کاربران auth شده دسترسی دارن
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),

    # 🕐 Throttling: محدود کردن تعداد درخواست‌ها
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle',
        'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '1000/day',  # هر کاربر auth شده روزانه 1000 درخواست
        'anon': '100/day',   # کاربران ناشناس روزانه 100 درخواست
    },

    # 📦 Pagination: استاندارد page number pagination
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,

    # 🔄 Parsers & Renderers: JSON به عنوان پیش‌فرض
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),

    # 💬 تنظیمات دیگر (اختیاری)
    'COERCE_DECIMAL_TO_STRING': False,
    'DATETIME_FORMAT': "%Y-%m-%dT%H:%M:%S.%fZ",
}
