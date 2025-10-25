from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample
from rest_framework import status
from account.serializers.models import CustomUserSerializer


class CustomUserListSchema:
    """Schema for listing and creating users"""

    @classmethod
    def get(cls):
        return extend_schema(
            summary="List Users",
            description="Retrieve a list of all registered users (admin only).",
            responses={
                status.HTTP_200_OK: OpenApiResponse(
                    response=CustomUserSerializer(many=True),
                    description="Users retrieved successfully.",
                    examples=[
                        OpenApiExample(
                            "Success",
                            value=[
                                {
                                    "id": 1,
                                    "username": "admin",
                                    "email": "admin@example.com",
                                    "first_name": "Admin",
                                    "last_name": "System",
                                },
                                {
                                    "id": 2,
                                    "username": "user1",
                                    "email": "user1@example.com",
                                    "first_name": "Ali",
                                    "last_name": "Rezaei",
                                },
                            ],
                        )
                    ],
                ),
                status.HTTP_403_FORBIDDEN: OpenApiResponse(
                    description="Forbidden (admin only)"
                ),
            },
        )

    @classmethod
    def post(cls):
        return extend_schema(
            summary="Create User",
            description="Add a new user with the provided information.",
            request=CustomUserSerializer,
            responses={
                status.HTTP_201_CREATED: OpenApiResponse(
                    response=CustomUserSerializer,
                    description="User created successfully.",
                    examples=[
                        OpenApiExample(
                            "Success",
                            value={
                                "id": 3,
                                "username": "new_user",
                                "email": "new_user@example.com",
                                "first_name": "Niloufar",
                                "last_name": "Mousavi",
                            },
                        )
                    ],
                ),
                status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                    description="Invalid input data",
                    examples=[
                        OpenApiExample(
                            "Error",
                            value={"email": ["This field must be unique."]},
                        ),
                    ],
                ),
            },
        )


class CustomUserDetailSchema:
    """Schema for retrieve, update, and delete user"""

    @classmethod
    def get(cls):
        return extend_schema(
            summary="Retrieve User",
            description="Retrieve user information by ID (pk).",
            responses={
                status.HTTP_200_OK: OpenApiResponse(
                    response=CustomUserSerializer,
                    description="User retrieved successfully.",
                ),
                status.HTTP_404_NOT_FOUND: OpenApiResponse(
                    description="User not found",
                    examples=[
                        OpenApiExample(
                            "Not Found",
                            value={"detail": "User not found"},
                        )
                    ],
                ),
            },
        )

    @classmethod
    def patch(cls):
        return extend_schema(
            summary="Update User",
            description="Partially update user information by ID.",
            request=CustomUserSerializer,
            responses={
                status.HTTP_200_OK: OpenApiResponse(
                    response=CustomUserSerializer,
                    description="User updated successfully.",
                ),
                status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                    description="Invalid input data",
                    examples=[
                        OpenApiExample(
                            "Error",
                            value={"email": ["Invalid email format."]},
                        ),
                    ],
                ),
                status.HTTP_404_NOT_FOUND: OpenApiResponse(
                    description="User not found",
                    examples=[
                        OpenApiExample(
                            "Not Found",
                            value={"detail": "User not found"},
                        ),
                    ],
                ),
            },
        )

    @classmethod
    def delete(cls):
        return extend_schema(
            summary="Delete User",
            description="Delete user by ID.",
            responses={
                status.HTTP_204_NO_CONTENT: OpenApiResponse(
                    description="User deleted successfully."
                ),
                status.HTTP_404_NOT_FOUND: OpenApiResponse(
                    description="User not found",
                    examples=[
                        OpenApiExample(
                            "Not Found",
                            value={"detail": "User not found"},
                        )
                    ],
                ),
            },
        )
