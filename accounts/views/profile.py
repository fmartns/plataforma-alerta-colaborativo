"""
Views para gerenciamento de perfil do usuário
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
import logging

from ..models import Profile
from ..serializers.user import UserSerializer, UserUpdateSerializer
from ..serializers.profile import ProfileUpdateSerializer
from ..docs.simple import USER_PROFILE_SIMPLE_SCHEMA, PROFILE_UPDATE_SIMPLE_SCHEMA

logger = logging.getLogger(__name__)


class UserProfileAPIView(APIView):
    """
    API para visualizar e atualizar dados básicos do usuário logado
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    @USER_PROFILE_SIMPLE_SCHEMA
    def get(self, request):
        """
        Retorna dados completos do usuário logado incluindo perfil
        """
        try:
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        except Exception as e:
            logger.error(
                f"Erro ao obter perfil do usuário {request.user.username}: {str(e)}"
            )
            return Response(
                {"message": "Erro ao obter dados do usuário", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @USER_PROFILE_SIMPLE_SCHEMA
    def patch(self, request):
        """
        Atualiza dados básicos do usuário (não inclui perfil)

        Campos atualizáveis:
        - first_name: Primeiro nome
        - last_name: Sobrenome
        - email: Email (deve ser único)
        """
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)

        if serializer.is_valid():
            try:
                user = serializer.save()
                logger.info(f"Dados do usuário atualizados: {user.username}")

                return Response(
                    {
                        "message": "Dados atualizados com sucesso",
                        "user": UserUpdateSerializer(user).data,
                    }
                )
            except Exception as e:
                logger.error(
                    f"Erro ao atualizar usuário {request.user.username}: {str(e)}"
                )
                return Response(
                    {"message": "Erro interno do servidor", "error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return Response(
            {"message": "Dados inválidos", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @USER_PROFILE_SIMPLE_SCHEMA
    def put(self, request):
        """
        Atualização completa dos dados básicos do usuário
        """
        serializer = UserUpdateSerializer(request.user, data=request.data)

        if serializer.is_valid():
            try:
                user = serializer.save()
                logger.info(f"Dados completos do usuário atualizados: {user.username}")

                return Response(
                    {
                        "message": "Dados atualizados com sucesso",
                        "user": UserUpdateSerializer(user).data,
                    }
                )
            except Exception as e:
                logger.error(
                    f"Erro ao atualizar usuário {request.user.username}: {str(e)}"
                )
                return Response(
                    {"message": "Erro interno do servidor", "error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return Response(
            {"message": "Dados inválidos", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ProfileUpdateAPIView(APIView):
    """
    API para visualizar e atualizar perfil do contribuinte
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileUpdateSerializer

    def get_profile(self, user):
        """
        Obtém o perfil do usuário ou retorna erro 404
        """
        return get_object_or_404(Profile, user=user)

    @PROFILE_UPDATE_SIMPLE_SCHEMA
    def get(self, request):
        """
        Retorna dados completos do perfil do contribuinte
        """
        try:
            profile = self.get_profile(request.user)
            serializer = ProfileUpdateSerializer(profile)
            return Response(serializer.data)
        except Exception as e:
            logger.error(
                f"Erro ao obter perfil do usuário {request.user.username}: {str(e)}"
            )
            return Response(
                {"message": "Erro ao obter perfil", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @PROFILE_UPDATE_SIMPLE_SCHEMA
    def patch(self, request):
        """
        Atualiza dados do perfil do contribuinte

        Campos atualizáveis:
        - foto: Foto de perfil
        - data_nascimento: Data de nascimento
        - telefone: Telefone de contato
        - endereco: Endereço completo
        - bairro: Bairro de Florianópolis
        - cep: CEP

        Nota: CPF não pode ser alterado após a criação
        """
        try:
            profile = self.get_profile(request.user)
            serializer = ProfileUpdateSerializer(
                profile, data=request.data, partial=True
            )

            if serializer.is_valid():
                try:
                    updated_profile = serializer.save()
                    logger.info(
                        f"Perfil atualizado: {updated_profile.user.username} - {updated_profile.get_cpf_formatado()}"
                    )

                    return Response(
                        {
                            "message": "Perfil atualizado com sucesso",
                            "profile": ProfileUpdateSerializer(updated_profile).data,
                        }
                    )
                except Exception as e:
                    logger.error(
                        f"Erro ao salvar perfil do usuário {request.user.username}: {str(e)}"
                    )
                    return Response(
                        {"message": "Erro interno do servidor", "error": str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )

            return Response(
                {"message": "Dados inválidos", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            logger.error(
                f"Erro ao atualizar perfil do usuário {request.user.username}: {str(e)}"
            )
            return Response(
                {"message": "Erro ao processar solicitação", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @PROFILE_UPDATE_SIMPLE_SCHEMA
    def put(self, request):
        """
        Atualização completa do perfil do contribuinte
        """
        try:
            profile = self.get_profile(request.user)
            serializer = ProfileUpdateSerializer(profile, data=request.data)

            if serializer.is_valid():
                try:
                    updated_profile = serializer.save()
                    logger.info(
                        f"Perfil completamente atualizado: {updated_profile.user.username}"
                    )

                    return Response(
                        {
                            "message": "Perfil atualizado com sucesso",
                            "profile": ProfileUpdateSerializer(updated_profile).data,
                        }
                    )
                except Exception as e:
                    logger.error(
                        f"Erro ao salvar perfil completo do usuário {request.user.username}: {str(e)}"
                    )
                    return Response(
                        {"message": "Erro interno do servidor", "error": str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )

            return Response(
                {"message": "Dados inválidos", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            logger.error(
                f"Erro ao atualizar perfil completo do usuário {request.user.username}: {str(e)}"
            )
            return Response(
                {"message": "Erro ao processar solicitação", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @PROFILE_UPDATE_SIMPLE_SCHEMA
    def delete(self, request):
        """
        Desativa o perfil do usuário (soft delete)
        """
        try:
            profile = self.get_profile(request.user)
            profile.ativo = False
            profile.save()

            logger.info(
                f"Perfil desativado: {profile.user.username} - {profile.get_cpf_formatado()}"
            )

            return Response(
                {
                    "message": "Perfil desativado com sucesso",
                    "profile_id": profile.id,
                    "active": profile.ativo,
                }
            )
        except Exception as e:
            logger.error(
                f"Erro ao desativar perfil do usuário {request.user.username}: {str(e)}"
            )
            return Response(
                {"message": "Erro ao desativar perfil", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
