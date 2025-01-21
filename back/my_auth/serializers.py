from my_auth.models import User
from django.core import exceptions
from django.contrib.auth.hashers import make_password
from django.contrib.auth import password_validation
from rest_framework import serializers


class AuthSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, max_length=150)
    first_name = serializers.CharField(required=False, max_length=150)
    last_name = serializers.CharField(required=False, max_length=150)
    email = serializers.EmailField(required=True, max_length=100)
    password = serializers.CharField(write_only=True, required=True, max_length=100)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "is_unknown_user",
            "is_expert",
            "is_admin",
        )
        read_only_fields = ("is_expert", "is_admin")

    def validate_password(self, value):
        errors = None
        try:
            password_validation.validate_password(password=value, user=User)
        except exceptions.ValidationError as e:
            errors = {"password": list(e.messages)}

        if errors:
            raise serializers.ValidationError(errors)
        return make_password(value)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "is_expert",
        )
        read_only_fields = fields
