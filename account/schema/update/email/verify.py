from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiResponse,
)
from rest_framework import status
from account.serializers.update.email import VerifyEmailUpdateSerializer


class VerifyEmailUpdateSchema:
    """
    Schema definitions for the VerifyEmailUpdateAPIView.
    """

    @classmethod
    def post(cls):
        return extend_schema(
            summary="Verify Email Change with OTP",
            description=(
                "This API endpoint is used to confirm the user's email change request. "
                "The user must provide the OTP code received on their new email address "
                "to verify and complete the email update process."
            ),
            request=VerifyEmailUpdateSerializer,
            responses={
                status.HTTP_200_OK: OpenApiResponse(
                    response=VerifyEmailUpdateSerializer,
                    description="Email successfully updated after OTP verification.",
                    examples=[
                        OpenApiExample(
                            name="Successful Verification",
                            summary="Email updated successfully.",
                            value={"detail": "Email updated successfully."},
                            response_only=True,
                            media_type="application/json",
                        ),
                    ],
                ),
                status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                    response=VerifyEmailUpdateSerializer,
                    description="Invalid OTP or incorrect input.",
                    examples=[
                        OpenApiExample(
                            name="Invalid OTP Code",
                            summary="OTP code is incorrect or expired.",
                            value={"otp_code": ["Invalid OTP code."]},
                            response_only=True,
                            media_type="application/json",
                        ),
                        OpenApiExample(
                            name="Missing OTP Field",
                            summary="OTP code not provided.",
                            value={"otp_code": ["This field is required."]},
                            response_only=True,
                            media_type="application/json",
                        ),
                    ],
                ),
                status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                    response=VerifyEmailUpdateSerializer,
                    description="User not authenticated.",
                    examples=[
                        OpenApiExample(
                            name="Unauthorized",
                            summary="User not logged in.",
                            value={"detail": "Authentication credentials were not provided."},
                            response_only=True,
                            media_type="application/json",
                        ),
                    ],
                ),
                status.HTTP_404_NOT_FOUND: OpenApiResponse(
                    response=VerifyEmailUpdateSerializer,
                    description="No pending email change request found or OTP expired.",
                    examples=[
                        OpenApiExample(
                            name="Request Not Found",
                            summary="Verification request expired or not found.",
                            value={"detail": "Email change request not found."},
                            response_only=True,
                            media_type="application/json",
                        ),
                    ],
                ),
            },
            examples=[
                OpenApiExample(
                    name="Request Example",
                    summary="Valid request example for verifying email change.",
                    description="Send your new email and OTP code to confirm email change.",
                    value={
                        "new_email": "newuser@example.com",
                        "otp_code": "123456"
                    },
                    request_only=True,
                    media_type="application/json",
                ),
            ],
            tags=["Email Update"],
        )
