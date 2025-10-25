from typing import Optional, Union
from django_redis import get_redis_connection
from django.core.exceptions import ImproperlyConfigured, ValidationError
from redis.exceptions import ConnectionError, TimeoutError, RedisError


class RedisService:
    """
    A high-level wrapper for Redis operations using `django-redis`.

    This service provides convenient and type-safe methods for setting,
    getting, incrementing, and deleting keys in Redis. It is designed
    for use in Django and DRF projects where Redis is used for caching,
    OTP handling, rate limiting, or similar use cases.

    Example:
        >>> redis_service = RedisService()
        >>> redis_service.set("otp:+989120000009", "123456", ttl=300)
        >>> otp = redis_service.get("otp:+989120000009")
        >>> print(otp)
        '123456'
        >>> redis_service.delete("otp:+989120000009")
    """

    def __init__(self, alias: str = "default"):
        """
        Initialize a RedisService instance.

        Args:
            alias (str): The cache alias defined in Django settings (default: "default").

        Raises:
            ImproperlyConfigured: If the Redis connection cannot be established.
        """
        try:
            self.connection = get_redis_connection(alias)
        except Exception as e:
            raise ImproperlyConfigured(f"Redis connection failed for alias '{alias}': {e}")

    # ------------------------------------------------------------------------
    # Core Redis Methods
    # ------------------------------------------------------------------------

    def set(self, key: str, value: Union[str, int, bytes], ttl: Optional[int] = None) -> None:
        """
        Set a key-value pair in Redis with an optional TTL (time-to-live).

        Args:
            key (str): Redis key.
            value (Union[str, int, bytes]): Value to store.
            ttl (Optional[int]): Expiration time in seconds (default: None — no expiration).

        Raises:
            ValidationError: If key or value is invalid.
            RedisError: If Redis operation fails.
        """
        if not key:
            raise ValidationError("Redis key cannot be empty.")

        try:
            self.connection.set(name=key, value=value, ex=ttl)
        except RedisError as e:
            raise RedisError(f"Failed to set key '{key}' in Redis: {e}")

    def get(self, key: str) -> Optional[str]:
        """
        Retrieve a value from Redis by key.

        Args:
            key (str): Redis key.

        Returns:
            Optional[str]: Decoded string value if found, otherwise None.

        Raises:
            RedisError: If Redis operation fails.
        """
        try:
            val = self.connection.get(key)
            return val.decode("utf-8") if val else None
        except RedisError as e:
            raise RedisError(f"Failed to get key '{key}' from Redis: {e}")

    def delete(self, key: str) -> None:
        """
        Delete a key from Redis.

        Args:
            key (str): Redis key to delete.

        Raises:
            RedisError: If Redis operation fails.
        """
        try:
            self.connection.delete(key)
        except RedisError as e:
            raise RedisError(f"Failed to delete key '{key}' from Redis: {e}")

    def incr(self, key: str) -> int:
        """
        Increment a numeric key in Redis by 1.

        Args:
            key (str): Redis key to increment.

        Returns:
            int: The new incremented value.

        Raises:
            RedisError: If Redis operation fails.
        """
        try:
            return int(self.connection.incr(key))
        except RedisError as e:
            raise RedisError(f"Failed to increment key '{key}' in Redis: {e}")

    def expire(self, key: str, ttl: int) -> None:
        """
        Set an expiration time (TTL) for a Redis key.

        Args:
            key (str): Redis key.
            ttl (int): Expiration time in seconds.

        Raises:
            RedisError: If Redis operation fails.
        """
        try:
            self.connection.expire(key, ttl)
        except RedisError as e:
            raise RedisError(f"Failed to set expiration for key '{key}': {e}")

    # ------------------------------------------------------------------------
    # Utility Methods
    # ------------------------------------------------------------------------

    def exists(self, key: str) -> bool:
        """
        Check if a Redis key exists.

        Args:
            key (str): Redis key.

        Returns:
            bool: True if the key exists, otherwise False.
        """
        try:
            return bool(self.connection.exists(key))
        except RedisError as e:
            raise RedisError(f"Failed to check existence of key '{key}': {e}")

    def ttl(self, key: str) -> Optional[int]:
        """
        Get the remaining TTL (time-to-live) of a Redis key.

        Args:
            key (str): Redis key.

        Returns:
            Optional[int]: TTL in seconds, or None if the key does not exist or has no expiration.
        """
        try:
            ttl = self.connection.ttl(key)
            return ttl if ttl >= 0 else None
        except RedisError as e:
            raise RedisError(f"Failed to retrieve TTL for key '{key}': {e}")
