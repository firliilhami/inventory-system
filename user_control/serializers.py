from rest_framework import serializers
from .models import CustomUser, ROLES


class CreateUSerSerializer(serializers.Serializer):
    email = serializers.EmailField()
    fullname = serializers.CharField()
    role = serializers.ChoiceField(ROLES)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(required=False)
    is_new_user = serializers.BooleanField(default=False, required=False)


class UpdatePasswordSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    password = serializers.CharField()


class CustomUSerSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        exclude = ("password", )

