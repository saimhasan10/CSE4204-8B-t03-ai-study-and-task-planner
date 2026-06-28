from django.contrib.auth.models import User
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "confirm_password",
        ]

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError({
                "password": "Password and confirm password do not match."
            })

        if User.objects.filter(username=data["username"]).exists():
            raise serializers.ValidationError({
                "username": "This username is already taken."
            })

        if data.get("email") and User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError({
                "email": "This email is already registered."
            })

        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
        ]
        read_only_fields = ["id", "username"]

    def validate_email(self, value):
        user = self.instance

        if value and User.objects.exclude(id=user.id).filter(email=value).exists():
            raise serializers.ValidationError("This email is already used by another account.")

        return value