import logging

from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from account.models.custom_user import CustomUser


logger = logging.getLogger(__name__)


class RequestEmailUpdateSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    new_email = serializers.EmailField()
    new_email_confirm = serializers.EmailField()

    def validate_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            logger.warning(f"User {user.id} entered incorrect password for email change.")
            raise serializers.ValidationError(_("Password is incorrect."))
        return value

    def validate(self, attrs):
        new_email = attrs["new_email"]
        confirm_email = attrs["new_email_confirm"]

        if new_email != confirm_email:
            raise serializers.ValidationError({"new_email_confirm": _("Emails do not match.")})

        if CustomUser.objects.filter(email__iexact=new_email).exists():
            raise serializers.ValidationError({"new_email": _("This email is already in use.")})

        return attrs
    