from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import os
from .validators import validate_file_size, validate_media_type


def alert_media_path(instance, filename):
    """
    Define o caminho para upload de mídias dos alertas
    """
    return f"alerts/{instance.user.username}/{filename}"


class Alert(models.Model):
    """
    Modelo para alertas de desastres enviados pelos usuários
    """
    
    CATEGORIA_CHOICES = [
        ('enchente', 'Enchente'),
        ('deslizamento', 'Deslizamento'),
        ('incendio', 'Incêndio'),
        ('tempestade', 'Tempestade'),
        ('acidente', 'Acidente'),
        ('outros', 'Outros'),
    ]
    
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('analisando', 'Analisando'),
        ('aprovado', 'Aprovado'),
        ('rejeitado', 'Rejeitado'),
        ('publicado', 'Publicado'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Usuário",
        related_name="alerts"
    )
    
    categoria = models.CharField(
        max_length=50,
        choices=CATEGORIA_CHOICES,
        verbose_name="Categoria",
        help_text="Categoria do alerta"
    )
    
    descricao = models.TextField(
        verbose_name="Descrição",
        help_text="Descrição detalhada do alerta"
    )
    
    media = models.FileField(
        upload_to=alert_media_path,
        blank=True,
        null=True,
        validators=[validate_file_size, validate_media_type],
        verbose_name="Mídia",
        help_text="Foto ou vídeo do alerta (máx. 50MB)"
    )
    
    localizacao = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Localização",
        help_text="Localização do incidente"
    )
    
    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=8,
        blank=True,
        null=True,
        verbose_name="Latitude"
    )
    
    longitude = models.DecimalField(
        max_digits=11,
        decimal_places=8,
        blank=True,
        null=True,
        verbose_name="Longitude"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pendente',
        verbose_name="Status",
        help_text="Status da análise do alerta"
    )
    
    prioridade = models.IntegerField(
        default=1,
        choices=[(1, 'Baixa'), (2, 'Média'), (3, 'Alta'), (4, 'Crítica')],
        verbose_name="Prioridade"
    )
    
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo"
    )
    
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )
    
    data_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Atualização"
    )
    
    class Meta:
        verbose_name = "Alerta"
        verbose_name_plural = "Alertas"
        ordering = ["-data_criacao"]
    
    def __str__(self):
        return f"{self.get_categoria_display()} - {self.user.username} ({self.data_criacao.strftime('%d/%m/%Y %H:%M')})"
    
    def get_media_type(self):
        """
        Retorna o tipo de mídia (image ou video)
        """
        if not self.media:
            return None
        
        ext = os.path.splitext(self.media.name)[1].lower()
        if ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
            return 'image'
        elif ext in ['.mp4', '.avi', '.mov', '.wmv', '.flv']:
            return 'video'
        return 'unknown'


class Post(models.Model):
    """
    Modelo para posts da Defesa Civil baseados em alertas
    """
    
    STATUS_CHOICES = [
        ('rascunho', 'Rascunho'),
        ('publicado', 'Publicado'),
        ('arquivado', 'Arquivado'),
    ]
    
    titulo = models.CharField(
        max_length=200,
        verbose_name="Título",
        help_text="Título do post"
    )
    
    conteudo = models.TextField(
        verbose_name="Conteúdo",
        help_text="Conteúdo do post"
    )
    
    alert = models.ForeignKey(
        Alert,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Alerta Relacionado",
        related_name="posts",
        help_text="Alerta que originou este post"
    )
    
    autor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Autor",
        related_name="posts",
        help_text="Administrador que criou o post"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='rascunho',
        verbose_name="Status"
    )
    
    destaque = models.BooleanField(
        default=False,
        verbose_name="Destaque",
        help_text="Post em destaque no feed"
    )
    
    permite_comentarios = models.BooleanField(
        default=True,
        verbose_name="Permite Comentários"
    )
    
    visualizacoes = models.PositiveIntegerField(
        default=0,
        verbose_name="Visualizações"
    )
    
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )
    
    data_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Atualização"
    )
    
    data_publicacao = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Data de Publicação"
    )
    
    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ["-data_publicacao", "-data_criacao"]
    
    def __str__(self):
        return f"{self.titulo} - {self.get_status_display()}"
    
    def save(self, *args, **kwargs):
        if self.status == 'publicado' and not self.data_publicacao:
            from django.utils import timezone
            self.data_publicacao = timezone.now()
        super().save(*args, **kwargs)


class Comment(models.Model):
    """
    Modelo para comentários nos posts
    """
    
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name="Post",
        related_name="comments"
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Usuário",
        related_name="comments"
    )
    
    conteudo = models.TextField(
        verbose_name="Comentário",
        help_text="Conteúdo do comentário"
    )
    
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Comentário Pai",
        related_name="replies",
        help_text="Comentário ao qual este é uma resposta"
    )
    
    aprovado = models.BooleanField(
        default=True,
        verbose_name="Aprovado",
        help_text="Comentário aprovado para exibição"
    )
    
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo"
    )
    
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )
    
    data_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Atualização"
    )
    
    class Meta:
        verbose_name = "Comentário"
        verbose_name_plural = "Comentários"
        ordering = ["data_criacao"]
    
    def __str__(self):
        return f"Comentário de {self.user.username} em '{self.post.titulo}'"
    
    def get_replies_count(self):
        """
        Retorna o número de respostas a este comentário
        """
        return self.replies.filter(ativo=True, aprovado=True).count()
