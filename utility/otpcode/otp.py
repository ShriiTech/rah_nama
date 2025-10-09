
import random
from django.conf import settings
from django_redis import get_redis_connection
from datetime import timedelta

def generate_otp(length=6):
    """تولید عدد OTP رندوم با تعداد رقم مشخص"""
    # عدد تصادفی با طول مشخص، مثلاً 6 رقم
    otp = random.randint(10**(length - 1), (10**length) - 1)
    return str(otp)

def get_redis():
    return get_redis_connection("default")

def cache_otp(phone_number: str, otp: str, ttl: int = None):
    """ذخیره otp در redis با کلید مشخص."""
    r = get_redis()
    ttl = ttl if ttl is not None else getattr(settings, "OTP_TTL", 300)
    key = f"otp:{phone_number}"
    r.set(key, otp, ex=ttl)

def get_cached_otp(phone_number: str):
    r = get_redis()
    key = f"otp:{phone_number}"
    val = r.get(key)
    if val is None:
        return None
    return val.decode()

def invalidate_otp(phone_number: str):
    r = get_redis()
    r.delete(f"otp:{phone_number}")

def increment_request_count(phone_number: str):
    """افزایش شمارنده درخواست OTP و برگشت مقدار فعلی"""
    r = get_redis()
    key = f"otp:req:{phone_number}"
    window = getattr(settings, "OTP_REQUEST_WINDOW", 3600)
    # INCR and set expiration on first set
    value = r.incr(key)
    if value == 1:
        r.expire(key, window)
    return int(value)

def get_request_count(phone_number: str):
    r = get_redis()
    key = f"otp:req:{phone_number}"
    v = r.get(key)
    return int(v) if v else 0
