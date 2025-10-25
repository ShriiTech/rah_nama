from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiResponse,
)
from rest_framework import status

from account.serializers.auth.jwt.otp import RequestOTPSerializer


class RequestOTPSchema:
    """
    Schema definitions for the RequestOTPAPIView.
    """

    @classmethod
    def post(cls):
        return extend_schema(
            summary="Request OTP Code",
            description=(
                "Generates and sends a one-time password (OTP) to the provided phone number. "
                "Includes a simple rate limit to prevent excessive requests. "
                "If the request limit is exceeded, a 429 Too Many Requests error is returned."
            ),
            request=RequestOTPSerializer,
            responses={
                status.HTTP_200_OK: OpenApiResponse(
                    response=RequestOTPSerializer,
                    description="OTP successfully generated and sent.",
                    examples=[
                        OpenApiExample(
                            name="OTP Sent",
                            summary="OTP code generated successfully.",
                            value={
                                "detail": "کد OTP ارسال شد.",
                                "otp": "123456",
                            },
                            response_only=True,
                            media_type="application/json",
                        ),
                    ],
                ),
                status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                    response=RequestOTPSerializer,
                    description="Invalid phone number or bad input data.",
                    examples=[
                        OpenApiExample(
                            name="Missing Phone Number",
                            summary="Phone number not provided.",
                            value={"phone_number": ["This field is required."]},
                            response_only=True,
                            media_type="application/json",
                        ),
                        OpenApiExample(
                            name="Invalid Phone Format",
                            summary="Invalid phone number format.",
                            value={"phone_number": ["Invalid phone number format."]},
                            response_only=True,
                            media_type="application/json",
                        ),
                    ],
                ),
                status.HTTP_429_TOO_MANY_REQUESTS: OpenApiResponse(
                    response=RequestOTPSerializer,
                    description="Too many OTP requests for this phone number.",
                    examples=[
                        OpenApiExample(
                            name="Rate Limit Exceeded",
                            summary="Request frequency too high.",
                            value={
                                "detail": "تعداد درخواست‌های OTP برای این شماره بیش از حد مجاز است. بعداً تلاش کنید."
                            },
                            response_only=True,
                            media_type="application/json",
                        ),
                    ],
                ),
            },
            examples=[
                OpenApiExample(
                    name="Request Example",
                    summary="Valid request example for OTP generation",
                    description="Send a phone number to receive a one-time password (OTP).",
                    value={"phone_number": "+989121234567"},
                    request_only=True,
                    media_type="application/json",
                ),
            ],
            tags=["Jwt Authentication"],
        )
