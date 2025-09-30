"""
Views administrativas para o app alerts
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta
import logging

from ..models import Alert, Post, Comment
from ..serializers import (
    AlertListSerializer,
    AlertUpdateSerializer,
    PostListSerializer,
    CommentListSerializer
)

logger = logging.getLogger(__name__)


class AdminAlertListAPIView(APIView):
    """
    API administrativa para gerenciar alertas
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = AlertListSerializer
    
    def get(self, request):
        """
        Listar todos os alertas para administradores
        """
        try:
            queryset = Alert.objects.filter(ativo=True).select_related('user')
            
            status_filter = request.query_params.get('status')
            categoria = request.query_params.get('categoria')
            prioridade = request.query_params.get('prioridade')
            usuario = request.query_params.get('usuario')
            search = request.query_params.get('search')
            
            if status_filter:
                queryset = queryset.filter(status=status_filter)
            
            if categoria:
                queryset = queryset.filter(categoria=categoria)
            
            if prioridade:
                queryset = queryset.filter(prioridade=prioridade)
            
            if usuario:
                queryset = queryset.filter(user__username__icontains=usuario)
            
            if search:
                queryset = queryset.filter(
                    Q(descricao__icontains=search) | 
                    Q(localizacao__icontains=search) |
                    Q(user__username__icontains=search)
                )
            
            ordering = request.query_params.get('ordering', '-data_criacao')
            queryset = queryset.order_by(ordering)
            
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
                    },
                    'filters': {
                        'status_options': Alert.STATUS_CHOICES,
                        'categoria_options': Alert.CATEGORIA_CHOICES,
                        'prioridade_options': [(1, 'Baixa'), (2, 'Média'), (3, 'Alta'), (4, 'Crítica')]
                    }
                }
            })
            
        except Exception as e:
            logger.error(f"Erro ao listar alertas (admin): {str(e)}")
            return Response({
                'success': False,
                'message': 'Erro interno do servidor'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def patch(self, request, alert_id):
        """
        Atualizar status de alerta (administradores)
        """
        try:
            try:
                alert = Alert.objects.get(id=alert_id, ativo=True)
            except Alert.DoesNotExist:
                return Response({
                    'success': False,
                    'message': 'Alerta não encontrado'
                }, status=status.HTTP_404_NOT_FOUND)
            
            allowed_fields = ['status', 'prioridade']
            update_data = {k: v for k, v in request.data.items() if k in allowed_fields}
            
            serializer = AlertUpdateSerializer(alert, data=update_data, partial=True)
            
            if serializer.is_valid():
                old_status = alert.status
                serializer.save()
                
                logger.info(
                    f"Alerta {alert_id} atualizado por admin {request.user.username}: "
                    f"{old_status} -> {alert.status}"
                )
                
                return Response({
                    'success': True,
                    'message': 'Alerta atualizado com sucesso',
                    'data': {
                        'id': alert.id,
                        'status': alert.status,
                        'prioridade': alert.prioridade
                    }
                })
            
            return Response({
                'success': False,
                'message': 'Dados inválidos',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"Erro ao atualizar alerta (admin): {str(e)}")
            return Response({
                'success': False,
                'message': 'Erro interno do servidor'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminPostListAPIView(APIView):
    """
    API administrativa para gerenciar posts
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = PostListSerializer
    
    def get(self, request):
        """
        Listar posts com filtros administrativos
        """
        try:
            queryset = Post.objects.all().select_related('autor', 'alert')
            
            status_filter = request.query_params.get('status')
            autor = request.query_params.get('autor')
            destaque = request.query_params.get('destaque')
            search = request.query_params.get('search')
            data_inicio = request.query_params.get('data_inicio')
            data_fim = request.query_params.get('data_fim')
            
            if status_filter:
                queryset = queryset.filter(status=status_filter)
            
            if autor:
                queryset = queryset.filter(autor__username__icontains=autor)
            
            if destaque == 'true':
                queryset = queryset.filter(destaque=True)
            elif destaque == 'false':
                queryset = queryset.filter(destaque=False)
            
            if search:
                queryset = queryset.filter(
                    Q(titulo__icontains=search) | Q(conteudo__icontains=search)
                )
            
            if data_inicio:
                queryset = queryset.filter(data_criacao__date__gte=data_inicio)
            
            if data_fim:
                queryset = queryset.filter(data_criacao__date__lte=data_fim)
            
            ordering = request.query_params.get('ordering', '-data_criacao')
            queryset = queryset.order_by(ordering)
            
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 20))
            
            start = (page - 1) * page_size
            end = start + page_size
            
            total = queryset.count()
            posts = queryset[start:end]
            
            serializer = PostListSerializer(posts, many=True)
            
            return Response({
                'success': True,
                'data': {
                    'results': serializer.data,
                    'pagination': {
                        'page': page,
                        'page_size': page_size,
                        'total': total,
                        'pages': (total + page_size - 1) // page_size
                    },
                    'filters': {
                        'status_options': Post.STATUS_CHOICES
                    }
                }
            })
            
        except Exception as e:
            logger.error(f"Erro ao listar posts (admin): {str(e)}")
            return Response({
                'success': False,
                'message': 'Erro interno do servidor'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminCommentListAPIView(APIView):
    """
    API administrativa para gerenciar comentários
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = CommentListSerializer
    
    def get(self, request):
        """
        Listar comentários com filtros administrativos
        """
        try:
            queryset = Comment.objects.all().select_related('user', 'post')
            
            aprovado = request.query_params.get('aprovado')
            ativo = request.query_params.get('ativo')
            usuario = request.query_params.get('usuario')
            post_id = request.query_params.get('post')
            search = request.query_params.get('search')
            
            if aprovado == 'true':
                queryset = queryset.filter(aprovado=True)
            elif aprovado == 'false':
                queryset = queryset.filter(aprovado=False)
            
            if ativo == 'true':
                queryset = queryset.filter(ativo=True)
            elif ativo == 'false':
                queryset = queryset.filter(ativo=False)
            
            if usuario:
                queryset = queryset.filter(user__username__icontains=usuario)
            
            if post_id:
                queryset = queryset.filter(post__id=post_id)
            
            if search:
                queryset = queryset.filter(
                    Q(conteudo__icontains=search) |
                    Q(user__username__icontains=search) |
                    Q(post__titulo__icontains=search)
                )
            
            ordering = request.query_params.get('ordering', '-data_criacao')
            queryset = queryset.order_by(ordering)
            
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 20))
            
            start = (page - 1) * page_size
            end = start + page_size
            
            total = queryset.count()
            comments = queryset[start:end]
            
            serializer = CommentListSerializer(comments, many=True)
            
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
            logger.error(f"Erro ao listar comentários (admin): {str(e)}")
            return Response({
                'success': False,
                'message': 'Erro interno do servidor'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def patch(self, request, comment_id):
        """
        Moderar comentário (aprovar/reprovar)
        """
        try:
            try:
                comment = Comment.objects.get(id=comment_id)
            except Comment.DoesNotExist:
                return Response({
                    'success': False,
                    'message': 'Comentário não encontrado'
                }, status=status.HTTP_404_NOT_FOUND)
            
            action = request.data.get('action')
            
            if action == 'approve':
                comment.aprovado = True
                comment.save()
                message = 'Comentário aprovado com sucesso'
            elif action == 'reject':
                comment.aprovado = False
                comment.save()
                message = 'Comentário rejeitado com sucesso'
            elif action == 'delete':
                comment.ativo = False
                comment.save()
                message = 'Comentário excluído com sucesso'
            else:
                return Response({
                    'success': False,
                    'message': 'Ação inválida. Use: approve, reject ou delete'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            logger.info(
                f"Comentário {comment_id} moderado por admin {request.user.username}: {action}"
            )
            
            return Response({
                'success': True,
                'message': message,
                'data': {
                    'id': comment.id,
                    'aprovado': comment.aprovado,
                    'ativo': comment.ativo
                }
            })
            
        except Exception as e:
            logger.error(f"Erro ao moderar comentário: {str(e)}")
            return Response({
                'success': False,
                'message': 'Erro interno do servidor'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

