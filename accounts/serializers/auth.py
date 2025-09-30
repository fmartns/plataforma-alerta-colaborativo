"""
Serializers para autenticação JWT
"""

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ..models import Profile


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer customizado para JWT que inclui informações do perfil
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["username"] = user.username
        token["email"] = user.email
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name

        try:
            profile = user.profile
            token["has_profile"] = True
            token["cpf"] = profile.get_cpf_formatado()
            token["ativo"] = profile.ativo
        except Profile.DoesNotExist:
            token["has_profile"] = False

        return token
