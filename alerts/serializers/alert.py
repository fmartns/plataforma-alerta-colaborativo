"""
Serializers para o modelo Alert
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import Alert
from ..validators import (
    validate_alert_description,
    validate_coordinates,
    validate_priority,
    validate_florianopolis_location,
    get_media_info
)


class UserBasicSerializer(serializers.ModelSerializer):
    """
    Serializer básico para dados do usuário
    """
    nome_completo = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'nome_completo']
    
    def get_nome_completo(self, obj):
        return obj.get_full_name() or obj.username


class AlertSerializer(serializers.ModelSerializer):
    """
    Serializer completo para Alert
    """
    user = UserBasicSerializer(read_only=True)
    categoria_display = serializers.CharField(source='get_categoria_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    prioridade_display = serializers.CharField(source='get_prioridade_display', read_only=True)
    media_type = serializers.CharField(source='get_media_type', read_only=True)
    media_info = serializers.SerializerMethodField()
    tempo_desde_criacao = serializers.SerializerMethodField()
    
    class Meta:
        model = Alert
        fields = [
            'id', 'user', 'categoria', 'categoria_display', 'descricao',
            'media', 'media_type', 'media_info', 'localizacao', 'latitude',
            'longitude', 'status', 'status_display', 'prioridade',
            'prioridade_display', 'ativo', 'data_criacao', 'data_atualizacao',
            'tempo_desde_criacao'
        ]
    
    def get_media_info(self, obj):
        if obj.media:
            return get_media_info(obj.media)
        return None
    
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


class AlertCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para criação de Alert
    """
    
    class Meta:
        model = Alert
        fields = [
            'categoria', 'descricao', 'media', 'localizacao',
            'latitude', 'longitude', 'prioridade'
        ]
    
    def validate_descricao(self, value):
        validate_alert_description(value)
        return value
    
    def validate_localizacao(self, value):
        if value:
            validate_florianopolis_location(value)
        return value
    
    def validate_prioridade(self, value):
        validate_priority(value)
        return value
    
    def validate(self, attrs):
        latitude = attrs.get('latitude')
        longitude = attrs.get('longitude')
        
        if latitude is not None or longitude is not None:
            validate_coordinates(latitude, longitude)
        
        return attrs
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class AlertUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para atualização de Alert (apenas campos específicos)
    """
    
    class Meta:
        model = Alert
        fields = ['status', 'prioridade']
    
    def validate_prioridade(self, value):
        validate_priority(value)
        return value


class AlertListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listagem de Alerts
    """
    user = UserBasicSerializer(read_only=True)
    categoria_display = serializers.CharField(source='get_categoria_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    prioridade_display = serializers.CharField(source='get_prioridade_display', read_only=True)
    media_type = serializers.CharField(source='get_media_type', read_only=True)
    tem_media = serializers.SerializerMethodField()
    tempo_desde_criacao = serializers.SerializerMethodField()
    
    class Meta:
        model = Alert
        fields = [
            'id', 'user', 'categoria', 'categoria_display', 'descricao',
            'tem_media', 'media_type', 'localizacao', 'status', 'status_display',
            'prioridade', 'prioridade_display', 'data_criacao', 'tempo_desde_criacao'
        ]
    
    def get_tem_media(self, obj):
        return bool(obj.media)
    
    def get_tempo_desde_criacao(self, obj):
        from django.utils import timezone
        from datetime import timedelta
        
        now = timezone.now()
        diff = now - obj.data_criacao
        
        if diff < timedelta(minutes=1):
            return "Agora mesmo"
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


class AlertStatsSerializer(serializers.Serializer):
    """
    Serializer para estatísticas de alertas
    """
    total_alertas = serializers.IntegerField()
    alertas_pendentes = serializers.IntegerField()
    alertas_aprovados = serializers.IntegerField()
    alertas_hoje = serializers.IntegerField()
    alertas_semana = serializers.IntegerField()
    alertas_por_categoria = serializers.DictField()
    alertas_por_status = serializers.DictField()
    alertas_por_prioridade = serializers.DictField()
