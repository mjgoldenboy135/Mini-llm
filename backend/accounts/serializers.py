from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, OTPVerification


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "mobile", "name", "email", "role", "date_joined", "avatar"]
        read_only_fields = ["id", "date_joined", "role"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["mobile", "name", "email", "password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    mobile = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        from django.contrib.auth import authenticate
        user = authenticate(username=attrs["mobile"], password=attrs["password"])
        if not user:
            raise serializers.ValidationError("Invalid credentials.")
        if not user.is_active:
            raise serializers.ValidationError("Account is inactive.")
        refresh = RefreshToken.for_user(user)
        return {
            "user": UserSerializer(user).data,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }


class OTPRequestSerializer(serializers.Serializer):
    mobile = serializers.CharField()


class OTPVerifySerializer(serializers.Serializer):
    mobile = serializers.CharField()
    code = serializers.CharField(max_length=6)
