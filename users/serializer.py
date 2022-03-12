from django.contrib import auth
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from .models import NewUser


class UserRegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    message = serializers.SerializerMethodField()

    class Meta:
        model = NewUser
        fields = ["email", "role", "message", "password"]

    def get_message(self, obj):
        return (
            "Verification message has been sent to your email, please verify your email"
        )

    def create(self, validated_data):
        return NewUser.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = NewUser
        fields = ["token"]


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=200)
    password = serializers.CharField(max_length=200, write_only=True)
    tokens = serializers.SerializerMethodField()
    role = serializers.CharField(read_only=True)

    class Meta:
        model = NewUser
        fields = ["email", "password", "tokens", "role"]

    def get_tokens(self, obj):
        user = NewUser.objects.get(email=obj["email"])
        return {"refresh": user.tokens()["refresh"], "access": user.tokens()["access"]}

    def validate(self, attrs):
        email = attrs.get("email", "")
        password = attrs.get("password", "")

        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed("Invalid credentials, try again")
        if not user.is_active:
            raise AuthenticationFailed("Account disabled, contact admin")
        if not user.is_verified:
            raise AuthenticationFailed("Email is not verified")

        return {"email": user.email, "tokens": user.tokens, "role": user.role}


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = NewUser
        fields = ("email", "role", "password")

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)
        instance.save()

        return instance
