"""
Views para autenticação e registro
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth.models import User
import logging

from ..serializers.user import UserCreateSerializer
from ..docs.simple import USER_CREATE_SIMPLE_SCHEMA, USER_AVAILABILITY_SIMPLE_SCHEMA

logger = logging.getLogger(__name__)


class UserCreateAPIView(APIView):
    """
    API para criação de usuário com perfil usando APIView
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = UserCreateSerializer

    @USER_CREATE_SIMPLE_SCHEMA
    def post(self, request):
        """
        Cria um novo usuário com perfil completo

        Campos obrigatórios:
        - username: Nome de usuário único
        - email: Email único
        - password: Senha (mínimo 8 caracteres)
        - password_confirm: Confirmação da senha
        - first_name: Primeiro nome
        - last_name: Sobrenome
        - profile.cpf: CPF válido e único
        - profile.data_nascimento: Data de nascimento (mínimo 16 anos)

        Campos opcionais do perfil:
        - profile.foto: Foto de perfil
        - profile.telefone: Telefone de contato
        - profile.endereco: Endereço completo
        - profile.bairro: Bairro de Florianópolis
        - profile.cep: CEP
        """
        serializer = UserCreateSerializer(data=request.data)

        if serializer.is_valid():
            try:
                user = serializer.save()

                logger.info(
                    f"Novo usuário criado: {user.username} - {user.profile.get_cpf_formatado()}"
                )

                return Response(
                    {
                        "message": "Usuário criado com sucesso",
                        "user_id": user.id,
                        "username": user.username,
                        "profile_created": hasattr(user, "profile"),
                        "cpf": (
                            user.profile.get_cpf_formatado()
                            if hasattr(user, "profile")
                            else None
                        ),
                    },
                    status=status.HTTP_201_CREATED,
                )

            except Exception as e:
                logger.error(f"Erro ao criar usuário: {str(e)}")
                return Response(
                    {"message": "Erro interno do servidor", "error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return Response(
            {"message": "Dados inválidos", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @USER_AVAILABILITY_SIMPLE_SCHEMA
    def get(self, request):
        """
        Verifica disponibilidade de username e email
        """
        username = request.query_params.get("username")
        email = request.query_params.get("email")

        response_data = {}

        if username:
            response_data["username_available"] = not User.objects.filter(
                username=username
            ).exists()
            response_data["username"] = username

        if email:
            response_data["email_available"] = not User.objects.filter(
                email=email
            ).exists()
            response_data["email"] = email

        if not username and not email:
            return Response(
                {"message": "Forneça username ou email para verificar disponibilidade"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(response_data)
