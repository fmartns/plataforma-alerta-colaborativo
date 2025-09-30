"""
Views para o modelo Post
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Q, Count, F
from django.utils import timezone
from datetime import timedelta
import logging

from ..models import Post, Alert
from ..serializers import (
    PostSerializer,
    PostCreateSerializer,
    PostUpdateSerializer,
    PostListSerializer,
    PostStatsSerializer
)

logger = logging.getLogger(__name__)


class PostCreateAPIView(APIView):
    """
    API para criação de posts (apenas administradores)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = PostCreateSerializer
    
    def post(self, request):
        """
        Criar novo post da Defesa Civil
        """
        try:
            serializer = PostCreateSerializer(data=request.data, context={'request': request})
            
            if serializer.is_valid():
                post = serializer.save()
                
                logger.info(f"Post criado: {post.id} por admin {request.user.username}")
                
                response_serializer = PostSerializer(post)
                return Response({
                    'success': True,
                    'message': 'Post criado com sucesso',
                    'data': response_serializer.data
                }, status=status.HTTP_201_CREATED)
            
            return Response({
                'success': False,
                'message': 'Dados inválidos',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"Erro ao criar post: {str(e)}")
            return Response({
                'success': False,
                'message': 'Erro interno do servidor'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PostListAPIView(APIView):
    """
    API para listagem de posts (administradores)
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = PostListSerializer
    
    def get(self, request):
        """
        Listar todos os posts para administradores
        """
        try:
            queryset = Post.objects.all()
            
            status_filter = request.query_params.get('status')
            autor = request.query_params.get('autor')
            search = request.query_params.get('search')
            
            if status_filter:
                queryset = queryset.filter(status=status_filter)
            
            if autor:
                queryset = queryset.filter(autor__username__icontains=autor)
            
            if search:
                queryset = queryset.filter(
                    Q(titulo__icontains=search) | Q(conteudo__icontains=search)
                )
            
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
                    }
                }
            })
            
        except Exception as e:
            logger.error(f"Erro ao listar posts: {str(e)}")
            return Response({
                'success': False,
                'message': 'Erro interno do servidor'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PostDetailAPIView(APIView):
    """
    API para detalhes, atualização e exclusão de post
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = PostSerializer
    
    def get_object(self, post_id):
        """
        Buscar post
        """
        try:
            return Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return None
    
    def get(self, request, post_id):
        """
        Obter detalhes do post
        """
        try:
            post = self.get_object(post_id)
            
            if not post:
                return Response({
                    'success': False,
                    'message': 'Post não encontrado'
                }, status=status.HTTP_404_NOT_FOUND)
            
            serializer = PostSerializer(post)
            
            return Response({
                'success': True,
                'data': serializer.data
            })
            
        except Exception as e:
            logger.error(f"Erro ao obter post: {str(e)}")
            return Response({
                'success': False,
                'message': 'Erro interno do servidor'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def patch(self, request, post_id):
        """
        Atualizar post
        """
        try:
            post = self.get_object(post_id)
            
            if not post:
                return Response({
                    'success': False,
                    'message': 'Post não encontrado'
                }, status=status.HTTP_404_NOT_FOUND)
            
            serializer = PostUpdateSerializer(post, data=request.data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                
                response_serializer = PostSerializer(post)
                return Response({
                    'success': True,
                    'message': 'Post atualizado com sucesso',
                    'data': response_serializer.data
                })
            
            return Response({
                'success': False,
                'message': 'Dados inválidos',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"Erro ao atualizar post: {str(e)}")
            return Response({
                'success': False,
                'message': 'Erro interno do servidor'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, post_id):
        """
        Arquivar post
        """
        try:
            post = self.get_object(post_id)
            
            if not post:
                return Response({
                    'success': False,
                    'message': 'Post não encontrado'
                }, status=status.HTTP_404_NOT_FOUND)
            
            post.status = 'arquivado'
            post.save()
            
            logger.info(f"Post {post_id} arquivado por admin {request.user.username}")
            
            return Response({
                'success': True,
                'message': 'Post arquivado com sucesso'
            })
            
        except Exception as e:
            logger.error(f"Erro ao arquivar post: {str(e)}")
            return Response({
                'success': False,
                'message': 'Erro interno do servidor'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PostFeedAPIView(APIView):
    """
    API para feed público de posts
    """
    permission_classes = []
    serializer_class = PostListSerializer
    
    def get(self, request):
        """
        Obter feed público de posts publicados
        """
        try:
            queryset = Post.objects.filter(
                status='publicado',
                permite_comentarios=True
            ).select_related('autor', 'alert')
            
            search = request.query_params.get('search')
            destaque = request.query_params.get('destaque')
            
            if search:
                queryset = queryset.filter(
                    Q(titulo__icontains=search) | Q(conteudo__icontains=search)
                )
            
            if destaque == 'true':
                queryset = queryset.filter(destaque=True)
            
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 10))
            
            start = (page - 1) * page_size
            end = start + page_size
            
            total = queryset.count()
            posts = queryset[start:end]
            
            for post in posts:
                post.visualizacoes = F('visualizacoes') + 1
                post.save(update_fields=['visualizacoes'])
            
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
                    }
                }
            })
            
        except Exception as e:
            logger.error(f"Erro ao obter feed: {str(e)}")
            return Response({
                'success': False,
                'message': 'Erro interno do servidor'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request, post_id):
        """
        Visualizar post específico (incrementa contador)
        """
        try:
            post = Post.objects.filter(id=post_id, status='publicado').first()
            
            if not post:
                return Response({
                    'success': False,
                    'message': 'Post não encontrado'
                }, status=status.HTTP_404_NOT_FOUND)
            
            post.visualizacoes = F('visualizacoes') + 1
            post.save(update_fields=['visualizacoes'])
            
            post.refresh_from_db()
            serializer = PostSerializer(post)
            
            return Response({
                'success': True,
                'data': serializer.data
            })
            
        except Exception as e:
            logger.error(f"Erro ao visualizar post: {str(e)}")
            return Response({
                'success': False,
                'message': 'Erro interno do servidor'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PostStatsAPIView(APIView):
    """
    API para estatísticas de posts
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = PostStatsSerializer
    
    def get(self, request):
        """
        Obter estatísticas dos posts
        """
        try:
            all_posts = Post.objects.all()
            
            now = timezone.now()
            today = now.date()
            week_ago = now - timedelta(days=7)
            
            stats = {
                'total_posts': all_posts.count(),
                'posts_publicados': all_posts.filter(status='publicado').count(),
                'posts_rascunho': all_posts.filter(status='rascunho').count(),
                'posts_hoje': all_posts.filter(data_criacao__date=today).count(),
                'posts_semana': all_posts.filter(data_criacao__gte=week_ago).count(),
                'total_visualizacoes': sum(all_posts.values_list('visualizacoes', flat=True)),
                'total_comentarios': sum(
                    post.comments.filter(ativo=True, aprovado=True).count() 
                    for post in all_posts
                ),
            }
            
            mais_visualizados = all_posts.filter(status='publicado').order_by('-visualizacoes')[:5]
            stats['posts_mais_visualizados'] = [
                {
                    'id': post.id,
                    'titulo': post.titulo,
                    'visualizacoes': post.visualizacoes
                }
                for post in mais_visualizados
            ]
            
            mais_comentados = sorted(
                all_posts.filter(status='publicado'),
                key=lambda p: p.comments.filter(ativo=True, aprovado=True).count(),
                reverse=True
            )[:5]
            
            stats['posts_mais_comentados'] = [
                {
                    'id': post.id,
                    'titulo': post.titulo,
                    'comentarios': post.comments.filter(ativo=True, aprovado=True).count()
                }
                for post in mais_comentados
            ]
            
            serializer = PostStatsSerializer(stats)
            
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

