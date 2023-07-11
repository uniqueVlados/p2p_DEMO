from rest_framework import serializers

from .models import (
    User,
    SecretKey,
    )
from .utils import is_password_ok


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def validate_password(self, value):
        if not is_password_ok(value):
            raise serializers.ValidationError(
                'Пароль не соответствует требованиям. Необходимо минимум 8 символов и 1 заглавная буква'
                )
        return value


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128)

    def validate_password(self, value):
        if not is_password_ok(value):
            raise serializers.ValidationError(
                'Пароль не соответствует требованиям. Необходимо минимум 8 символов.'
                )
        return value


class UserPersonDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class PartnerSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=128, allow_blank=True)
    last_name = serializers.CharField(max_length=128, allow_blank=True)


class SecretKeyRetrieveSerializer(serializers.Serializer):
    secret_key = serializers.CharField(max_length=128)


class SecretKeysListSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format=('%d.%m.%Y, %H:%M'))

    class Meta:
        model = SecretKey
        fields = ['id', 'created_at', 'name', 'is_available']


class SecretKeySerializer(serializers.ModelSerializer):

    class Meta:
        model = SecretKey
        fields = ['name', 'is_available']


class SecretKeyGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = SecretKey
        fields = ['id', 'name', 'key', 'is_available']


class SecretKeyCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=32)
