"""
Serializers para o modelo Post
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import Post, Alert
from ..validators import validate_post_content
from .alert import AlertListSerializer


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer completo para Post
    """
    autor = serializers.StringRelatedField(read_only=True)
    autor_nome = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    alert = AlertListSerializer(read_only=True)
    comentarios_count = serializers.SerializerMethodField()
    tempo_desde_publicacao = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'titulo', 'conteudo', 'alert', 'autor', 'autor_nome',
            'status', 'status_display', 'destaque', 'permite_comentarios',
            'visualizacoes', 'comentarios_count', 'data_criacao',
            'data_atualizacao', 'data_publicacao', 'tempo_desde_publicacao'
        ]
    
    def get_autor_nome(self, obj):
        return obj.autor.get_full_name() or obj.autor.username
    
    def get_comentarios_count(self, obj):
        return obj.comments.filter(ativo=True, aprovado=True).count()
    
    def get_tempo_desde_publicacao(self, obj):
        if not obj.data_publicacao:
            return None
        
        from django.utils import timezone
        from datetime import timedelta
        
        now = timezone.now()
        diff = now - obj.data_publicacao
        
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
            return obj.data_publicacao.strftime("%d/%m/%Y às %H:%M")


class PostCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para criação de Post
    """
    alert_id = serializers.IntegerField(required=False, allow_null=True)
    
    class Meta:
        model = Post
        fields = [
            'titulo', 'conteudo', 'alert_id', 'status', 'destaque',
            'permite_comentarios'
        ]
    
    def validate_conteudo(self, value):
        validate_post_content(value)
        return value
    
    def validate_alert_id(self, value):
        if value is not None:
            try:
                Alert.objects.get(id=value)
            except Alert.DoesNotExist:
                raise serializers.ValidationError("Alerta não encontrado")
        return value
    
    def create(self, validated_data):
        alert_id = validated_data.pop('alert_id', None)
        validated_data['autor'] = self.context['request'].user
        
        if alert_id:
            validated_data['alert'] = Alert.objects.get(id=alert_id)
        
        return super().create(validated_data)


class PostUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para atualização de Post
    """
    
    class Meta:
        model = Post
        fields = [
            'titulo', 'conteudo', 'status', 'destaque', 'permite_comentarios'
        ]
    
    def validate_conteudo(self, value):
        validate_post_content(value)
        return value


class PostListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listagem de Posts
    """
    autor_nome = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    comentarios_count = serializers.SerializerMethodField()
    tempo_desde_publicacao = serializers.SerializerMethodField()
    conteudo_resumido = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'titulo', 'conteudo_resumido', 'autor_nome', 'status',
            'status_display', 'destaque', 'permite_comentarios', 'visualizacoes',
            'comentarios_count', 'data_publicacao', 'tempo_desde_publicacao'
        ]
    
    def get_autor_nome(self, obj):
        return obj.autor.get_full_name() or obj.autor.username
    
    def get_comentarios_count(self, obj):
        return obj.comments.filter(ativo=True, aprovado=True).count()
    
    def get_tempo_desde_publicacao(self, obj):
        if not obj.data_publicacao:
            return None
        
        from django.utils import timezone
        from datetime import timedelta
        
        now = timezone.now()
        diff = now - obj.data_publicacao
        
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
            return obj.data_publicacao.strftime("%d/%m")
    
    def get_conteudo_resumido(self, obj):
        if len(obj.conteudo) <= 200:
            return obj.conteudo
        return obj.conteudo[:200] + "..."


class PostStatsSerializer(serializers.Serializer):
    """
    Serializer para estatísticas de posts
    """
    total_posts = serializers.IntegerField()
    posts_publicados = serializers.IntegerField()
    posts_rascunho = serializers.IntegerField()
    posts_hoje = serializers.IntegerField()
    posts_semana = serializers.IntegerField()
    total_visualizacoes = serializers.IntegerField()
    total_comentarios = serializers.IntegerField()
    posts_mais_visualizados = serializers.ListField()
    posts_mais_comentados = serializers.ListField()

