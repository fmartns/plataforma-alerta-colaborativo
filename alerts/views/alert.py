"""
Views para o modelo Alert
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta
import logging

from ..models import Alert
from ..serializers import (
    AlertSerializer,
    AlertCreateSerializer,
    AlertUpdateSerializer,
    AlertListSerializer,
    AlertStatsSerializer
)
from ..docs.simple import (
    ALERT_CREATE_SIMPLE_SCHEMA,
    ALERT_LIST_SIMPLE_SCHEMA,
    ALERT_DETAIL_SIMPLE_SCHEMA,
    ALERT_UPDATE_SIMPLE_SCHEMA,
    ALERT_DELETE_SIMPLE_SCHEMA,
    ALERT_STATS_SIMPLE_SCHEMA
)

logger = logging.getLogger(__name__)


class AlertCreateAPIView(APIView):
    """
    API para criação de alertas pelos usuários
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    serializer_class = AlertCreateSerializer
    
    @ALERT_CREATE_SIMPLE_SCHEMA
    def post(self, request):
        """
        Criar novo alerta de desastre
        """
        try:
            serializer = AlertCreateSerializer(data=request.data, context={'request': request})
            
            if serializer.is_valid():
                alert = serializer.save()
                
                logger.info(f"Alerta criado: {alert.id} por usuário {request.user.username}")
                
                response_serializer = AlertSerializer(alert)
                return Response({
                    'success': True,
                    'message': 'Alerta criado com sucesso',
                    'data': response_serializer.data
                }, status=status.HTTP_201_CREATED)
            
            return Response({
                'success': False,
                'message': 'Dados inválidos',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"Erro ao criar alerta: {str(e)}")
            return Response({
                'success': False,
                'message': 'Erro interno do servidor'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AlertListAPIView(APIView):
    """
    API para listagem de alertas do usuário
    """
    permission_classes = [IsAuthenticated]
    serializer_class = AlertListSerializer
    
    def get(self, request):
        """
        Listar alertas do usuário autenticado
        """
        try:
            queryset = Alert.objects.filter(user=request.user, ativo=True)
            
            categoria = request.query_params.get('categoria')
            status_filter = request.query_params.get('status')
            prioridade = request.query_params.get('prioridade')
            
            if categoria:
                queryset = queryset.filter(categoria=categoria)
            
            if status_filter:
                queryset = queryset.filter(status=status_filter)
            
            if prioridade:
                queryset = queryset.filter(prioridade=prioridade)
            
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 20))
            
            start = (page - 1) * page_size
            end = start + page_size
            
            total = queryset.count()
            alerts = queryset[start:end]
            
            serializer = AlertListSerializer(alerts, many=True)
            
            return Response({
                'success': True,
                'data': {
                    'results': serializer.data,
                    'pagination': {
                        'page': page,
                        'page_size': page_size,
                        'total': total,
                        'pages': (total + page_size - 1) // page_size
                    }
                }
            })
            
        except Exception as e:
            logger.error(f"Erro ao listar alertas: {str(e)}")
            return Response({
                'success': False,
                'message': 'Erro interno do servidor'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AlertDetailAPIView(APIView):
    """
    API para detalhes, atualização e exclusão de alerta
    """
    permission_classes = [IsAuthenticated]
    serializer_class = AlertSerializer
    
    def get_object(self, alert_id, user):
        """
        Buscar alerta do usuário
        """
        try:
            return Alert.objects.get(id=alert_id, user=user, ativo=True)
        except Alert.DoesNotExist:
            return None
    
    def get(self, request, alert_id):
        """
        Obter detalhes do alerta
        """
        try:
            alert = self.get_object(alert_id, request.user)
            
            if not alert:
                return Response({
                    'success': False,
                    'message': 'Alerta não encontrado'
                }, status=status.HTTP_404_NOT_FOUND)
            
            serializer = AlertSerializer(alert)
            
            return Response({
                'success': True,
                'data': serializer.data
            })
            
        except Exception as e:
            logger.error(f"Erro ao obter alerta: {str(e)}")
            return Response({
                'success': False,
                'message': 'Erro interno do servidor'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def patch(self, request, alert_id):
        """
        Atualizar alerta (apenas status e prioridade para usuários)
        """
        try:
            alert = self.get_object(alert_id, request.user)
            
            if not alert:
                return Response({
                    'success': False,
                    'message': 'Alerta não encontrado'
                }, status=status.HTTP_404_NOT_FOUND)
            
            if alert.status != 'pendente':
                return Response({
                    'success': False,
                    'message': 'Alerta já foi processado e não pode ser alterado'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = AlertUpdateSerializer(alert, data=request.data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                
                response_serializer = AlertSerializer(alert)
                return Response({
                    'success': True,
                    'message': 'Alerta atualizado com sucesso',
                    'data': response_serializer.data
                })
            
            return Response({
                'success': False,
                'message': 'Dados inválidos',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"Erro ao atualizar alerta: {str(e)}")
            return Response({
                'success': False,
                'message': 'Erro interno do servidor'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, alert_id):
        """
        Excluir alerta (soft delete)
        """
        try:
            alert = self.get_object(alert_id, request.user)
            
            if not alert:
                return Response({
                    'success': False,
                    'message': 'Alerta não encontrado'
                }, status=status.HTTP_404_NOT_FOUND)
            
            if alert.status not in ['pendente', 'rejeitado']:
                return Response({
                    'success': False,
                    'message': 'Alerta já foi processado e não pode ser excluído'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            alert.ativo = False
            alert.save()
            
            logger.info(f"Alerta {alert_id} excluído por usuário {request.user.username}")
            
            return Response({
                'success': True,
                'message': 'Alerta excluído com sucesso'
            })
            
        except Exception as e:
            logger.error(f"Erro ao excluir alerta: {str(e)}")
            return Response({
                'success': False,
                'message': 'Erro interno do servidor'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AlertStatsAPIView(APIView):
    """
    API para estatísticas de alertas do usuário
    """
    permission_classes = [IsAuthenticated]
    serializer_class = AlertStatsSerializer
    
    def get(self, request):
        """
        Obter estatísticas dos alertas do usuário
        """
        try:
            user_alerts = Alert.objects.filter(user=request.user, ativo=True)
            
            now = timezone.now()
            today = now.date()
            week_ago = now - timedelta(days=7)
            
            stats = {
                'total_alertas': user_alerts.count(),
                'alertas_pendentes': user_alerts.filter(status='pendente').count(),
                'alertas_aprovados': user_alerts.filter(status='aprovado').count(),
                'alertas_hoje': user_alerts.filter(data_criacao__date=today).count(),
                'alertas_semana': user_alerts.filter(data_criacao__gte=week_ago).count(),
            }
            
            categorias = user_alerts.values('categoria').annotate(
                count=Count('categoria')
            ).order_by('-count')
            stats['alertas_por_categoria'] = {
                item['categoria']: item['count'] for item in categorias
            }
            
            status_counts = user_alerts.values('status').annotate(
                count=Count('status')
            ).order_by('-count')
            stats['alertas_por_status'] = {
                item['status']: item['count'] for item in status_counts
            }
            
            prioridades = user_alerts.values('prioridade').annotate(
                count=Count('prioridade')
            ).order_by('-count')
            stats['alertas_por_prioridade'] = {
                str(item['prioridade']): item['count'] for item in prioridades
            }
            
            serializer = AlertStatsSerializer(stats)
            
            return Response({
                'success': True,
                'data': serializer.data
            })
            
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas: {str(e)}")
            return Response({
                'success': False,
                'message': 'Erro interno do servidor'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
