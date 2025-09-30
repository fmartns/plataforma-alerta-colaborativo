"""
Serializers para o modelo Comment
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import Comment, Post
from ..validators import validate_comment_content


class UserCommentSerializer(serializers.ModelSerializer):
    """
    Serializer básico para dados do usuário em comentários
    """
    nome_completo = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'nome_completo']
    
    def get_nome_completo(self, obj):
        return obj.get_full_name() or obj.username


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer completo para Comment
    """
    user = UserCommentSerializer(read_only=True)
    post_titulo = serializers.CharField(source='post.titulo', read_only=True)
    parent_user = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()
    replies_count = serializers.CharField(source='get_replies_count', read_only=True)
    tempo_desde_criacao = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = [
            'id', 'post', 'post_titulo', 'user', 'conteudo', 'parent',
            'parent_user', 'replies', 'replies_count', 'aprovado', 'ativo',
            'data_criacao', 'data_atualizacao', 'tempo_desde_criacao'
        ]
    
    def get_parent_user(self, obj):
        if obj.parent:
            return UserCommentSerializer(obj.parent.user).data
        return None
    
    def get_replies(self, obj):
        if hasattr(obj, 'replies'):
            replies = obj.replies.filter(ativo=True, aprovado=True).order_by('data_criacao')
            return CommentListSerializer(replies, many=True, context=self.context).data
        return []
    
    def get_tempo_desde_criacao(self, obj):
        from django.utils import timezone
        from datetime import timedelta
        
        now = timezone.now()
        diff = now - obj.data_criacao
        
        if diff < timedelta(minutes=1):
            return "Agora mesmo"
        elif diff < timedelta(hours=1):
            minutes = int(diff.total_seconds() / 60)
            return f"{minutes} minuto{'s' if minutes != 1 else ''} atrás"
        elif diff < timedelta(days=1):
            hours = int(diff.total_seconds() / 3600)
            return f"{hours} hora{'s' if hours != 1 else ''} atrás"
        elif diff < timedelta(days=7):
            days = diff.days
            return f"{days} dia{'s' if days != 1 else ''} atrás"
        else:
            return obj.data_criacao.strftime("%d/%m/%Y às %H:%M")


class CommentCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para criação de Comment
    """
    post_id = serializers.IntegerField()
    parent_id = serializers.IntegerField(required=False, allow_null=True)
    
    class Meta:
        model = Comment
        fields = ['post_id', 'conteudo', 'parent_id']
    
    def validate_conteudo(self, value):
        validate_comment_content(value)
        return value
    
    def validate_post_id(self, value):
        try:
            post = Post.objects.get(id=value, status='publicado')
            if not post.permite_comentarios:
                raise serializers.ValidationError("Este post não permite comentários")
        except Post.DoesNotExist:
            raise serializers.ValidationError("Post não encontrado ou não publicado")
        return value
    
    def validate_parent_id(self, value):
        if value is not None:
            try:
                parent = Comment.objects.get(id=value, ativo=True, aprovado=True)
                if parent.parent is not None:
                    raise serializers.ValidationError("Não é possível responder a uma resposta")
            except Comment.DoesNotExist:
                raise serializers.ValidationError("Comentário pai não encontrado")
        return value
    
    def validate(self, attrs):
        post_id = attrs.get('post_id')
        parent_id = attrs.get('parent_id')
        
        if parent_id:
            try:
                parent = Comment.objects.get(id=parent_id)
                if parent.post.id != post_id:
                    raise serializers.ValidationError("Comentário pai deve pertencer ao mesmo post")
            except Comment.DoesNotExist:
                pass
        
        return attrs
    
    def create(self, validated_data):
        post_id = validated_data.pop('post_id')
        parent_id = validated_data.pop('parent_id', None)
        
        validated_data['user'] = self.context['request'].user
        validated_data['post'] = Post.objects.get(id=post_id)
        
        if parent_id:
            validated_data['parent'] = Comment.objects.get(id=parent_id)
        
        return super().create(validated_data)


class CommentUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para atualização de Comment
    """
    
    class Meta:
        model = Comment
        fields = ['conteudo']
    
    def validate_conteudo(self, value):
        validate_comment_content(value)
        return value


class CommentListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listagem de Comments
    """
    user = UserCommentSerializer(read_only=True)
    replies_count = serializers.CharField(source='get_replies_count', read_only=True)
    tempo_desde_criacao = serializers.SerializerMethodField()
    conteudo_resumido = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = [
            'id', 'user', 'conteudo_resumido', 'parent', 'replies_count',
            'data_criacao', 'tempo_desde_criacao'
        ]
    
    def get_tempo_desde_criacao(self, obj):
        from django.utils import timezone
        from datetime import timedelta
        
        now = timezone.now()
        diff = now - obj.data_criacao
        
        if diff < timedelta(minutes=1):
            return "Agora"
        elif diff < timedelta(hours=1):
            minutes = int(diff.total_seconds() / 60)
            return f"{minutes}min"
        elif diff < timedelta(days=1):
            hours = int(diff.total_seconds() / 3600)
            return f"{hours}h"
        elif diff < timedelta(days=7):
            days = diff.days
            return f"{days}d"
        else:
            return obj.data_criacao.strftime("%d/%m")
    
    def get_conteudo_resumido(self, obj):
        if len(obj.conteudo) <= 100:
            return obj.conteudo
        return obj.conteudo[:100] + "..."


class CommentStatsSerializer(serializers.Serializer):
    """
    Serializer para estatísticas de comentários
    """
    total_comentarios = serializers.IntegerField()
    comentarios_aprovados = serializers.IntegerField()
    comentarios_pendentes = serializers.IntegerField()
    comentarios_hoje = serializers.IntegerField()
    comentarios_semana = serializers.IntegerField()
    usuarios_mais_ativos = serializers.ListField()
    posts_mais_comentados = serializers.ListField()

