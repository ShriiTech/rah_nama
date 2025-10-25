from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiExample,
)
from rest_framework import status

from account.serializers.auth.jwt.otp.verify_serializers import VerifyOTPSerializer


class VerifyOTPSchema:
    """
    Schema definitions for the VerifyOTPAPIView.
    """

    @classmethod
    def post(cls):
        return extend_schema(
            summary="Verify OTP Code",
            description=(
                "Verifies the provided OTP code for the given phone number. "
                "If the OTP is valid, a new user will be created (if not already existing), "
                "and JWT access & refresh tokens will be returned. "
                "If the OTP is invalid or expired, an appropriate error message is returned."
            ),
            request=VerifyOTPSerializer,
            responses={
                status.HTTP_200_OK: OpenApiResponse(
                    response=None,
                    description="OTP verified successfully. Returns JWT tokens.",
                    examples=[
                        OpenApiExample(
                            name="OTP Verified",
                            summary="Successful verification response.",
                            value={
                                "access": "eyJ0eXAiOiJKV1QiLCJh...",
                                "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                            },
                            response_only=True,
                            media_type="application/json",
                        ),
                    ],
                ),
                status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                    response=None,
                    description="Invalid or expired OTP code.",
                    examples=[
                        OpenApiExample(
                            name="Invalid OTP",
                            summary="OTP code does not match cached value.",
                            value={"detail": "کد اشتباه است."},
                            response_only=True,
                            media_type="application/json",
                        ),
                        OpenApiExample(
                            name="Expired or Missing OTP",
                            summary="OTP code not found or expired.",
                            value={"detail": "کد منقضی شده یا وجود ندارد."},
                            response_only=True,
                            media_type="application/json",
                        ),
                        OpenApiExample(
                            name="Invalid Input Data",
                            summary="Request missing required fields.",
                            value={
                                "phone_number": ["This field is required."],
                                "otp": ["This field is required."],
                            },
                            response_only=True,
                            media_type="application/json",
                        ),
                    ],
                ),
            },
            tags=["Jwt Authentication"],
        )
