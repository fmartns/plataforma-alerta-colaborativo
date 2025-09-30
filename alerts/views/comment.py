"""
Views para o modelo Comment
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta
import logging

from ..models import Comment, Post
from ..serializers import (
    CommentSerializer,
    CommentCreateSerializer,
    CommentUpdateSerializer,
    CommentListSerializer,
    CommentStatsSerializer
)

logger = logging.getLogger(__name__)


class CommentCreateAPIView(APIView):
    """
    API para criação de comentários
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CommentCreateSerializer
    
    def post(self, request):
        """
        Criar novo comentário
        """
        try:
            serializer = CommentCreateSerializer(data=request.data, context={'request': request})
            
            if serializer.is_valid():
                comment = serializer.save()
                
                logger.info(f"Comentário criado: {comment.id} por usuário {request.user.username}")
                
                response_serializer = CommentSerializer(comment)
                return Response({
                    'success': True,
                    'message': 'Comentário criado com sucesso',
                    'data': response_serializer.data
                }, status=status.HTTP_201_CREATED)
            
            return Response({
                'success': False,
                'message': 'Dados inválidos',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"Erro ao criar comentário: {str(e)}")
            return Response({
                'success': False,
                'message': 'Erro interno do servidor'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CommentListAPIView(APIView):
    """
    API para listagem de comentários de um post
    """
    permission_classes = []
    serializer_class = CommentListSerializer
    
    def get(self, request, post_id):
        """
        Listar comentários de um post específico
        """
        try:
            try:
                post = Post.objects.get(id=post_id, status='publicado')
            except Post.DoesNotExist:
                return Response({
                    'success': False,
                    'message': 'Post não encontrado'
                }, status=status.HTTP_404_NOT_FOUND)
            
            if not post.permite_comentarios:
                return Response({
                    'success': False,
                    'message': 'Este post não permite comentários'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            queryset = Comment.objects.filter(
                post=post,
                ativo=True,
                aprovado=True,
                parent=None
            ).select_related('user', 'post').prefetch_related('replies')
            
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 20))
            
            start = (page - 1) * page_size
            end = start + page_size
            
            total = queryset.count()
            comments = queryset[start:end]
            
            serializer = CommentSerializer(comments, many=True)
            
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
            logger.error(f"Erro ao listar comentários: {str(e)}")
            return Response({
                'success': False,
                'message': 'Erro interno do servidor'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CommentDetailAPIView(APIView):
    """
    API para detalhes, atualização e exclusão de comentário
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    
    def get_object(self, comment_id, user):
        """
        Buscar comentário do usuário
        """
        try:
            return Comment.objects.get(id=comment_id, user=user, ativo=True)
        except Comment.DoesNotExist:
            return None
    
    def get(self, request, comment_id):
        """
        Obter detalhes do comentário
        """
        try:
            comment = self.get_object(comment_id, request.user)
            
            if not comment:
                return Response({
                    'success': False,
                    'message': 'Comentário não encontrado'
                }, status=status.HTTP_404_NOT_FOUND)
            
            serializer = CommentSerializer(comment)
            
            return Response({
                'success': True,
                'data': serializer.data
            })
            
        except Exception as e:
            logger.error(f"Erro ao obter comentário: {str(e)}")
            return Response({
                'success': False,
                'message': 'Erro interno do servidor'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def patch(self, request, comment_id):
        """
        Atualizar comentário
        """
        try:
            comment = self.get_object(comment_id, request.user)
            
            if not comment:
                return Response({
                    'success': False,
                    'message': 'Comentário não encontrado'
                }, status=status.HTTP_404_NOT_FOUND)
            
            time_limit = timezone.now() - timedelta(minutes=15)
            if comment.data_criacao < time_limit:
                return Response({
                    'success': False,
                    'message': 'Comentário só pode ser editado até 15 minutos após a criação'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = CommentUpdateSerializer(comment, data=request.data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                
                response_serializer = CommentSerializer(comment)
                return Response({
                    'success': True,
                    'message': 'Comentário atualizado com sucesso',
                    'data': response_serializer.data
                })
            
            return Response({
                'success': False,
                'message': 'Dados inválidos',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"Erro ao atualizar comentário: {str(e)}")
            return Response({
                'success': False,
                'message': 'Erro interno do servidor'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, comment_id):
        """
        Excluir comentário (soft delete)
        """
        try:
            comment = self.get_object(comment_id, request.user)
            
            if not comment:
                return Response({
                    'success': False,
                    'message': 'Comentário não encontrado'
                }, status=status.HTTP_404_NOT_FOUND)
            
            time_limit = timezone.now() - timedelta(hours=1)
            if comment.data_criacao < time_limit:
                return Response({
                    'success': False,
                    'message': 'Comentário só pode ser excluído até 1 hora após a criação'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            comment.ativo = False
            comment.save()
            
            logger.info(f"Comentário {comment_id} excluído por usuário {request.user.username}")
            
            return Response({
                'success': True,
                'message': 'Comentário excluído com sucesso'
            })
            
        except Exception as e:
            logger.error(f"Erro ao excluir comentário: {str(e)}")
            return Response({
                'success': False,
                'message': 'Erro interno do servidor'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CommentStatsAPIView(APIView):
    """
    API para estatísticas de comentários
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = CommentStatsSerializer
    
    def get(self, request):
        """
        Obter estatísticas dos comentários
        """
        try:
            all_comments = Comment.objects.all()
            
            now = timezone.now()
            today = now.date()
            week_ago = now - timedelta(days=7)
            
            stats = {
                'total_comentarios': all_comments.count(),
                'comentarios_aprovados': all_comments.filter(aprovado=True, ativo=True).count(),
                'comentarios_pendentes': all_comments.filter(aprovado=False, ativo=True).count(),
                'comentarios_hoje': all_comments.filter(data_criacao__date=today).count(),
                'comentarios_semana': all_comments.filter(data_criacao__gte=week_ago).count(),
            }
            
            usuarios_ativos = all_comments.filter(
                ativo=True, aprovado=True
            ).values('user__username').annotate(
                count=Count('user')
            ).order_by('-count')[:10]
            
            stats['usuarios_mais_ativos'] = [
                {
                    'username': item['user__username'],
                    'comentarios': item['count']
                }
                for item in usuarios_ativos
            ]
            
            posts_comentados = all_comments.filter(
                ativo=True, aprovado=True
            ).values('post__titulo', 'post__id').annotate(
                count=Count('post')
            ).order_by('-count')[:10]
            
            stats['posts_mais_comentados'] = [
                {
                    'id': item['post__id'],
                    'titulo': item['post__titulo'],
                    'comentarios': item['count']
                }
                for item in posts_comentados
            ]
            
            serializer = CommentStatsSerializer(stats)
            
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

