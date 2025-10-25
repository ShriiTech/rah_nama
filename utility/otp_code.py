import random
from typing import Optional, Union

from django.conf import settings
from django.core.exceptions import ValidationError
from redis.exceptions import RedisError

from utility.redis import RedisService


class OTPGenerator:
    """
    A secure and configurable One-Time Password (OTP) generator.

    Attributes:
        length (int): The number of digits in the OTP (default: 6).

    Example:
        >>> generator = OTPGenerator(length=6)
        >>> otp = generator.generate()
        >>> print(otp)
        '573492'
    """

    def __init__(self, length: int = 6):
        """
        Initialize the OTP generator.

        Args:
            length (int): Length of the OTP. Must be between 4 and 8 digits.

        Raises:
            ValueError: If the provided length is out of valid range.
        """
        if not (4 <= length <= 8):
            raise ValueError("OTP length must be between 4 and 8 digits.")
        self.length = length

    def generate(self) -> str:
        """
        Generate a random numeric OTP with the configured length.

        Returns:
            str: The generated OTP as a string.
        """
        return str(random.randint(10 ** (self.length - 1), (10 ** self.length) - 1))


class OTPService:
    """
    A service class to handle OTP creation, caching, verification, and rate limiting.

    This class uses Redis as a backend to store OTPs and track the number of OTP requests
    per phone number, ensuring secure and rate-limited OTP management.

    Example:
        >>> otp_service = OTPService()
        >>> otp = otp_service.generate_and_cache_otp("+989120000009")
        >>> otp_service.verify_otp("+989120000009", otp)
        True
    """

    def __init__(self, redis_service: Optional[RedisService] = None):
        """
        Initialize the OTP service with Redis and configuration values.

        Args:
            redis_service (Optional[RedisService]): Custom RedisService instance for testing.
        """
        self.redis = redis_service or RedisService()
        self.ttl = getattr(settings, "OTP_TTL", 120)  # default 5 minutes
        self.request_window = getattr(settings, "OTP_REQUEST_WINDOW", 3600)  # 1 hour
        self.max_requests = getattr(settings, "OTP_MAX_REQUESTS", 5)

    # ------------------------------------------------------------------------
    # Internal Key Builders
    # ------------------------------------------------------------------------
    def _otp_key(self, phone_number: str) -> str:
        """Return the Redis key for storing OTPs."""
        return f"otp:{phone_number}"

    def _request_key(self, phone_number: str) -> str:
        """Return the Redis key for tracking OTP request counts."""
        return f"otp:req:{phone_number}"

    # ------------------------------------------------------------------------
    # OTP Core Methods
    # ------------------------------------------------------------------------
    def cache_otp(self, phone_number: str, otp: str, ttl: Optional[int] = None) -> None:
        """
        Cache the generated OTP in Redis with an optional TTL (default 5 minutes).

        Args:
            phone_number (str): The user's phone number.
            otp (str): The OTP to store.
            ttl (Optional[int]): Custom time-to-live for the OTP.

        Raises:
            RedisError: If the Redis operation fails.
        """
        ttl = ttl or self.ttl
        try:
            self.redis.set(self._otp_key(phone_number), otp, ttl)
        except RedisError as e:
            raise RedisError(f"Failed to cache OTP for {phone_number}: {e}")

    def get_cached_otp(self, phone_number: str) -> Optional[str]:
        """
        Retrieve a cached OTP for a given phone number.

        Args:
            phone_number (str): The user's phone number.

        Returns:
            Optional[str]: The cached OTP if found, otherwise None.
        """
        try:
            return self.redis.get(self._otp_key(phone_number))
        except RedisError as e:
            raise RedisError(f"Failed to retrieve OTP for {phone_number}: {e}")

    def invalidate_otp(self, phone_number: str) -> None:
        """
        Delete the cached OTP after successful verification.

        Args:
            phone_number (str): The user's phone number.

        Raises:
            RedisError: If Redis operation fails.
        """
        try:
            self.redis.delete(self._otp_key(phone_number))
        except RedisError as e:
            raise RedisError(f"Failed to invalidate OTP for {phone_number}: {e}")

    # ------------------------------------------------------------------------
    # OTP Request Limiting
    # ------------------------------------------------------------------------
    def increment_request_count(self, phone_number: str) -> int:
        """
        Increment the number of OTP requests for a phone number.

        This method also sets an expiration window for counting requests.

        Args:
            phone_number (str): The user's phone number.

        Returns:
            int: The updated request count.

        Raises:
            RedisError: If Redis operation fails.
        """
        key = self._request_key(phone_number)
        try:
            count = self.redis.incr(key)
            if count == 1:
                self.redis.expire(key, self.request_window)
            return int(count)
        except RedisError as e:
            raise RedisError(f"Failed to increment OTP request count for {phone_number}: {e}")

    def get_request_count(self, phone_number: str) -> int:
        """
        Get the current number of OTP requests made by a phone number.

        Args:
            phone_number (str): The user's phone number.

        Returns:
            int: Number of requests in the current rate window.
        """
        val = self.redis.get(self._request_key(phone_number))
        return int(val) if val else 0

    def can_request_otp(self, phone_number: str, max_requests: Optional[int] = None) -> bool:
        """
        Check whether the user can request a new OTP.

        Args:
            phone_number (str): The user's phone number.
            max_requests (Optional[int]): Custom max allowed requests (default from settings).

        Returns:
            bool: True if allowed, False otherwise.
        """
        max_requests = max_requests or self.max_requests
        return self.get_request_count(phone_number) < max_requests

    # ------------------------------------------------------------------------
    # High-Level Utility Methods
    # ------------------------------------------------------------------------
    def generate_and_cache_otp(self, phone_number: str) -> str:
        """
        Generate a new OTP and cache it in Redis, respecting rate limits.

        Args:
            phone_number (str): The user's phone number.

        Returns:
            str: The generated OTP.

        Raises:
            ValidationError: If request limit is exceeded.
            RedisError: If Redis operation fails.
        """
        if not self.can_request_otp(phone_number):
            raise ValidationError("Too many OTP requests. Please try again later.")

        otp = OTPGenerator().generate()
        self.cache_otp(phone_number, otp)
        self.increment_request_count(phone_number)
        return otp

    def verify_otp(self, phone_number: str, otp: str) -> bool:
        """
        Verify a user-provided OTP against the cached one.

        Args:
            phone_number (str): The user's phone number.
            otp (str): The OTP provided by the user.

        Returns:
            bool: True if OTP matches and is valid, False otherwise.
        """
        cached_otp = self.get_cached_otp(phone_number)
        if cached_otp is None:
            return False
        if otp != cached_otp:
            return False
        self.invalidate_otp(phone_number)
        return True
