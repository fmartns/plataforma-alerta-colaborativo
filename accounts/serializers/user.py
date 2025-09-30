"""
Serializers para modelo User
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from .profile import ProfileSerializer
from ..models import Profile


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo User com perfil
    """

    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "date_joined",
            "last_login",
            "profile",
        ]
        read_only_fields = ["date_joined", "last_login"]


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para criação de usuário com perfil
    """

    profile = ProfileSerializer()
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "password_confirm",
            "profile",
        ]

    def validate(self, attrs):
        """
        Valida se as senhas coincidem
        """
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError("As senhas não coincidem.")
        return attrs

    def validate_email(self, value):
        """
        Valida se o email é único
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email já está em uso.")
        return value

    def validate_username(self, value):
        """
        Valida se o username é único
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Este nome de usuário já está em uso.")
        return value

    def create(self, validated_data):
        """
        Cria usuário e perfil
        """
        profile_data = validated_data.pop("profile")
        validated_data.pop("password_confirm")

        user = User.objects.create_user(**validated_data)

        Profile.objects.create(user=user, **profile_data)

        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para atualização de dados básicos do usuário
    """

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

    def validate_email(self, value):
        """
        Valida se o email é único (exceto para o próprio usuário)
        """
        if self.instance and self.instance.email == value:
            return value

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email já está em uso.")
        return value
