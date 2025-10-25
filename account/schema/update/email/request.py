from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiResponse,
)
from rest_framework import status

from account.serializers.update.email.request_email_update_serializers import RequestEmailUpdateSerializer


class RequestEmailUpdateSchema:
    """
    Schema definitions for the RequestEmailUpdateAPIView.
    """

    @classmethod
    def post(cls):
        return extend_schema(
            summary="Request Email Change Verification Code",
            description=(
                "Allows an authenticated user to request an email change. "
                "A verification code is sent to the new email address. "
                "Until verification, the user's old email remains active."
            ),
            request=RequestEmailUpdateSerializer,
            responses={
                status.HTTP_201_CREATED: OpenApiResponse(
                    response=RequestEmailUpdateSerializer,
                    description="Verification code successfully sent to the new email address.",
                    examples=[
                        OpenApiExample(
                            name="Verification Code Sent",
                            summary="Email verification code sent successfully.",
                            value={"detail": "Verification code sent to new email."},
                            response_only=True,
                            media_type="application/json",
                        ),
                    ],
                ),
                status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                    response=RequestEmailUpdateSerializer,
                    description="Invalid input or incorrect email format.",
                    examples=[
                        OpenApiExample(
                            name="Invalid Email Format",
                            summary="The provided email address is invalid.",
                            value={"new_email": ["Invalid email format."]},
                            response_only=True,
                            media_type="application/json",
                        ),
                        OpenApiExample(
                            name="Missing Email Field",
                            summary="Email field not provided.",
                            value={"new_email": ["This field is required."]},
                            response_only=True,
                            media_type="application/json",
                        ),
                    ],
                ),
                status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                    response=RequestEmailUpdateSerializer,
                    description="User not authenticated.",
                    examples=[
                        OpenApiExample(
                            name="Unauthorized Access",
                            summary="Authentication credentials were not provided.",
                            value={"detail": "Authentication credentials were not provided."},
                            response_only=True,
                            media_type="application/json",
                        ),
                    ],
                ),
                status.HTTP_409_CONFLICT: OpenApiResponse(
                    response=RequestEmailUpdateSerializer,
                    description="The provided email is already associated with another account.",
                    examples=[
                        OpenApiExample(
                            name="Email Already Exists",
                            summary="Conflict due to duplicate email.",
                            value={"detail": "Email already in use."},
                            response_only=True,
                            media_type="application/json",
                        ),
                    ],
                ),
            },
            examples=[
                OpenApiExample(
                    name="Request Example",
                    summary="Valid request example for email change verification.",
                    description="Send a new email address to receive a verification code.",
                    value={"new_email": "newuser@example.com"},
                    request_only=True,
                    media_type="application/json",
                ),
            ],
            tags=["Email Update"],
        )
