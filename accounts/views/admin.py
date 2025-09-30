"""
Views administrativas para gerenciamento de usuários e estatísticas
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.core.paginator import Paginator
import logging

from ..models import Profile
from ..serializers.profile import ProfileListSerializer
from ..docs.simple import PROFILES_LIST_SIMPLE_SCHEMA, STATS_SIMPLE_SCHEMA

logger = logging.getLogger(__name__)


class ProfileListAPIView(APIView):
    """
    API para listar perfis de contribuintes (apenas para administradores)
    """

    permission_classes = [permissions.IsAdminUser]

    @PROFILES_LIST_SIMPLE_SCHEMA
    def get(self, request):
        """
        Lista contribuintes com filtros opcionais e paginação

        Filtros disponíveis:
        - bairro: Filtrar por bairro específico
        - ativo: Filtrar por status ativo (true/false)
        - search: Buscar por nome ou CPF
        - page: Número da página
        - page_size: Itens por página (padrão: 20, máximo: 100)
        """
        try:
            queryset = Profile.objects.select_related("user").order_by("-data_cadastro")

            queryset = self._apply_filters(request, queryset)

            page = int(request.query_params.get("page", 1))
            page_size = min(int(request.query_params.get("page_size", 20)), 100)

            paginator = Paginator(queryset, page_size)
            page_obj = paginator.get_page(page)

            serializer = ProfileListSerializer(page_obj, many=True)

            next_url = None
            previous_url = None

            if page_obj.has_next():
                next_url = (
                    f"{request.build_absolute_uri()}?page={page_obj.next_page_number()}"
                )
                if request.query_params:
                    params = request.query_params.copy()
                    params["page"] = page_obj.next_page_number()
                    next_url = f"{request.build_absolute_uri().split('?')[0]}?{params.urlencode()}"

            if page_obj.has_previous():
                previous_url = f"{request.build_absolute_uri()}?page={page_obj.previous_page_number()}"
                if request.query_params:
                    params = request.query_params.copy()
                    params["page"] = page_obj.previous_page_number()
                    previous_url = f"{request.build_absolute_uri().split('?')[0]}?{params.urlencode()}"

            return Response(
                {
                    "count": paginator.count,
                    "next": next_url,
                    "previous": previous_url,
                    "page": page,
                    "page_size": page_size,
                    "total_pages": paginator.num_pages,
                    "results": serializer.data,
                }
            )

        except Exception as e:
            logger.error(f"Erro ao listar perfis: {str(e)}")
            return Response(
                {"message": "Erro ao listar contribuintes", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def _apply_filters(self, request, queryset):
        """
        Aplica filtros na queryset
        """
        bairro = request.query_params.get("bairro")
        if bairro:
            queryset = queryset.filter(bairro__icontains=bairro)

        ativo = request.query_params.get("ativo")
        if ativo is not None:
            ativo_bool = ativo.lower() in ("true", "1", "yes")
            queryset = queryset.filter(ativo=ativo_bool)

        search = request.query_params.get("search")
        if search:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search)
                | Q(user__last_name__icontains=search)
                | Q(user__username__icontains=search)
                | Q(cpf__icontains=search)
            )

        return queryset


class UserStatsAPIView(APIView):
    """
    API para estatísticas de usuários e contribuintes (apenas para administradores)
    """

    permission_classes = [permissions.IsAdminUser]

    @STATS_SIMPLE_SCHEMA
    def get(self, request):
        """
        Retorna estatísticas completas do sistema

        Inclui:
        - Total de usuários
        - Total de perfis
        - Perfis ativos/inativos
        - Top 10 bairros com mais contribuintes
        - Registros mensais (últimos 6 meses)
        - Distribuição de idades
        """
        try:
            total_users = User.objects.count()
            total_profiles = Profile.objects.count()
            active_profiles = Profile.objects.filter(ativo=True).count()
            inactive_profiles = total_profiles - active_profiles

            neighborhoods_stats = (
                Profile.objects.values("bairro")
                .annotate(count=Count("bairro"))
                .exclude(bairro="")
                .order_by("-count")[:10]
            )

            from django.utils import timezone
            from datetime import timedelta

            six_months_ago = timezone.now() - timedelta(days=180)
            monthly_registrations = (
                Profile.objects.filter(data_cadastro__gte=six_months_ago)
                .extra(select={"month": "strftime('%%Y-%%m', data_cadastro)"})
                .values("month")
                .annotate(count=Count("id"))
                .order_by("month")
            )

            age_distribution = self._get_age_distribution()

            data = {
                "total_users": total_users,
                "total_profiles": total_profiles,
                "active_profiles": active_profiles,
                "inactive_profiles": inactive_profiles,
                "completion_rate": (
                    round((total_profiles / total_users * 100), 2)
                    if total_users > 0
                    else 0
                ),
                "top_neighborhoods": list(neighborhoods_stats),
                "monthly_registrations": list(monthly_registrations),
                "age_distribution": age_distribution,
                "generated_at": timezone.now().isoformat(),
            }

            logger.info(f"Estatísticas geradas por {request.user.username}")
            return Response(data)

        except Exception as e:
            logger.error(f"Erro ao gerar estatísticas: {str(e)}")
            return Response(
                {"message": "Erro ao gerar estatísticas", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def _get_age_distribution(self):
        """
        Calcula distribuição de idades dos contribuintes
        """
        try:
            from datetime import date

            today = date.today()

            age_ranges = {
                "16-25": 0,
                "26-35": 0,
                "36-45": 0,
                "46-55": 0,
                "56-65": 0,
                "65+": 0,
            }

            profiles = Profile.objects.filter(ativo=True).select_related("user")

            for profile in profiles:
                age = (
                    today.year
                    - profile.data_nascimento.year
                    - (
                        (today.month, today.day)
                        < (profile.data_nascimento.month, profile.data_nascimento.day)
                    )
                )

                if 16 <= age <= 25:
                    age_ranges["16-25"] += 1
                elif 26 <= age <= 35:
                    age_ranges["26-35"] += 1
                elif 36 <= age <= 45:
                    age_ranges["36-45"] += 1
                elif 46 <= age <= 55:
                    age_ranges["46-55"] += 1
                elif 56 <= age <= 65:
                    age_ranges["56-65"] += 1
                elif age > 65:
                    age_ranges["65+"] += 1

            return age_ranges

        except Exception as e:
            logger.error(f"Erro ao calcular distribuição de idades: {str(e)}")
            return {}


class InactiveProfilesAPIView(APIView):
    """
    API para listar perfis inativos (apenas para administradores)
    """

    permission_classes = [permissions.IsAdminUser]
    serializer_class = ProfileListSerializer

    @PROFILES_LIST_SIMPLE_SCHEMA
    def get(self, request):
        """
        Lista contribuintes inativos com paginação
        """
        try:
            queryset = (
                Profile.objects.filter(ativo=False)
                .select_related("user")
                .order_by("-data_atualizacao")
            )

            page = int(request.query_params.get("page", 1))
            page_size = min(int(request.query_params.get("page_size", 20)), 100)

            paginator = Paginator(queryset, page_size)
            page_obj = paginator.get_page(page)

            serializer = ProfileListSerializer(page_obj, many=True)

            return Response(
                {
                    "count": paginator.count,
                    "page": page,
                    "page_size": page_size,
                    "total_pages": paginator.num_pages,
                    "results": serializer.data,
                }
            )

        except Exception as e:
            logger.error(f"Erro ao listar perfis inativos: {str(e)}")
            return Response(
                {"message": "Erro ao listar contribuintes inativos", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @PROFILES_LIST_SIMPLE_SCHEMA
    def patch(self, request):
        """
        Reativa um contribuinte inativo
        """
        try:
            profile_id = request.data.get("profile_id")
            if not profile_id:
                return Response(
                    {"message": "ID do perfil é obrigatório"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            profile = Profile.objects.get(id=profile_id, ativo=False)
            profile.ativo = True
            profile.save()

            logger.info(
                f"Perfil reativado por {request.user.username}: {profile.user.username} - {profile.get_cpf_formatado()}"
            )

            return Response(
                {
                    "message": "Contribuinte reativado com sucesso",
                    "profile": ProfileListSerializer(profile).data,
                }
            )

        except Profile.DoesNotExist:
            return Response(
                {"message": "Perfil não encontrado ou já está ativo"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            logger.error(f"Erro ao reativar perfil: {str(e)}")
            return Response(
                {"message": "Erro ao reativar contribuinte", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
