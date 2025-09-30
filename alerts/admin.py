from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Alert, Post, Comment


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    """
    Admin para gerenciar alertas
    """
    list_display = (
        'id', 'get_usuario', 'categoria', 'get_descricao_resumida',
        'get_media_preview', 'status', 'prioridade', 'data_criacao'
    )
    
    list_filter = (
        'categoria', 'status', 'prioridade', 'ativo', 'data_criacao'
    )
    
    search_fields = (
        'user__username', 'user__first_name', 'user__last_name',
        'descricao', 'localizacao'
    )
    
    readonly_fields = (
        'data_criacao', 'data_atualizacao', 'get_media_preview',
        'get_media_info', 'get_coordenadas'
    )
    
    fieldsets = (
        ('Usuário', {
            'fields': ('user',)
        }),
        ('Informações do Alerta', {
            'fields': ('categoria', 'descricao', 'status', 'prioridade')
        }),
        ('Mídia', {
            'fields': ('media', 'get_media_preview', 'get_media_info')
        }),
        ('Localização', {
            'fields': ('localizacao', 'latitude', 'longitude', 'get_coordenadas')
        }),
        ('Status', {
            'fields': ('ativo',)
        }),
        ('Datas', {
            'fields': ('data_criacao', 'data_atualizacao'),
            'classes': ('collapse',)
        })
    )
    
    actions = ['aprovar_alertas', 'rejeitar_alertas', 'marcar_como_analisando']
    
    def get_usuario(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_usuario.short_description = 'Usuário'
    get_usuario.admin_order_field = 'user__username'
    
    def get_descricao_resumida(self, obj):
        if len(obj.descricao) > 50:
            return obj.descricao[:50] + '...'
        return obj.descricao
    get_descricao_resumida.short_description = 'Descrição'
    
    def get_media_preview(self, obj):
        if obj.media:
            media_type = obj.get_media_type()
            if media_type == 'image':
                return format_html(
                    '<img src="{}" style="max-width: 100px; max-height: 100px;" />',
                    obj.media.url
                )
            elif media_type == 'video':
                return format_html(
                    '<video width="100" height="100" controls><source src="{}" /></video>',
                    obj.media.url
                )
        return 'Sem mídia'
    get_media_preview.short_description = 'Preview'
    
    def get_media_info(self, obj):
        if obj.media:
            from .validators import get_media_info
            info = get_media_info(obj.media)
            return f"Tipo: {info['type']}, Tamanho: {info['size_formatted']}"
        return 'Sem mídia'
    get_media_info.short_description = 'Informações da Mídia'
    
    def get_coordenadas(self, obj):
        if obj.latitude and obj.longitude:
            return f"Lat: {obj.latitude}, Lng: {obj.longitude}"
        return 'Não informado'
    get_coordenadas.short_description = 'Coordenadas'
    
    def aprovar_alertas(self, request, queryset):
        updated = queryset.update(status='aprovado')
        self.message_user(request, f'{updated} alerta(s) aprovado(s).')
    aprovar_alertas.short_description = 'Aprovar alertas selecionados'
    
    def rejeitar_alertas(self, request, queryset):
        updated = queryset.update(status='rejeitado')
        self.message_user(request, f'{updated} alerta(s) rejeitado(s).')
    rejeitar_alertas.short_description = 'Rejeitar alertas selecionados'
    
    def marcar_como_analisando(self, request, queryset):
        updated = queryset.update(status='analisando')
        self.message_user(request, f'{updated} alerta(s) marcado(s) como analisando.')
    marcar_como_analisando.short_description = 'Marcar como analisando'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Admin para gerenciar posts
    """
    list_display = (
        'id', 'titulo', 'get_autor', 'status', 'destaque',
        'permite_comentarios', 'visualizacoes', 'get_comentarios_count',
        'data_publicacao'
    )
    
    list_filter = (
        'status', 'destaque', 'permite_comentarios', 'data_criacao', 'data_publicacao'
    )
    
    search_fields = (
        'titulo', 'conteudo', 'autor__username', 'autor__first_name', 'autor__last_name'
    )
    
    readonly_fields = (
        'data_criacao', 'data_atualizacao', 'data_publicacao',
        'visualizacoes', 'get_comentarios_count', 'get_alert_link'
    )
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'conteudo', 'autor')
        }),
        ('Relacionamentos', {
            'fields': ('alert', 'get_alert_link')
        }),
        ('Configurações', {
            'fields': ('status', 'destaque', 'permite_comentarios')
        }),
        ('Estatísticas', {
            'fields': ('visualizacoes', 'get_comentarios_count'),
            'classes': ('collapse',)
        }),
        ('Datas', {
            'fields': ('data_criacao', 'data_atualizacao', 'data_publicacao'),
            'classes': ('collapse',)
        })
    )
    
    actions = ['publicar_posts', 'arquivar_posts', 'marcar_destaque', 'remover_destaque']
    
    def get_autor(self, obj):
        return obj.autor.get_full_name() or obj.autor.username
    get_autor.short_description = 'Autor'
    get_autor.admin_order_field = 'autor__username'
    
    def get_comentarios_count(self, obj):
        return obj.comments.filter(ativo=True, aprovado=True).count()
    get_comentarios_count.short_description = 'Comentários'
    
    def get_alert_link(self, obj):
        if obj.alert:
            url = reverse('admin:alerts_alert_change', args=[obj.alert.id])
            return format_html('<a href="{}">Ver Alerta #{}</a>', url, obj.alert.id)
        return 'Nenhum alerta relacionado'
    get_alert_link.short_description = 'Alerta Relacionado'
    
    def publicar_posts(self, request, queryset):
        updated = queryset.update(status='publicado')
        self.message_user(request, f'{updated} post(s) publicado(s).')
    publicar_posts.short_description = 'Publicar posts selecionados'
    
    def arquivar_posts(self, request, queryset):
        updated = queryset.update(status='arquivado')
        self.message_user(request, f'{updated} post(s) arquivado(s).')
    arquivar_posts.short_description = 'Arquivar posts selecionados'
    
    def marcar_destaque(self, request, queryset):
        updated = queryset.update(destaque=True)
        self.message_user(request, f'{updated} post(s) marcado(s) como destaque.')
    marcar_destaque.short_description = 'Marcar como destaque'
    
    def remover_destaque(self, request, queryset):
        updated = queryset.update(destaque=False)
        self.message_user(request, f'{updated} post(s) removido(s) do destaque.')
    remover_destaque.short_description = 'Remover destaque'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin para gerenciar comentários
    """
    list_display = (
        'id', 'get_usuario', 'get_post_titulo', 'get_conteudo_resumido',
        'get_parent_info', 'aprovado', 'ativo', 'data_criacao'
    )
    
    list_filter = (
        'aprovado', 'ativo', 'data_criacao', 'post__status'
    )
    
    search_fields = (
        'user__username', 'user__first_name', 'user__last_name',
        'conteudo', 'post__titulo'
    )
    
    readonly_fields = (
        'data_criacao', 'data_atualizacao', 'get_replies_count',
        'get_post_link', 'get_parent_link'
    )
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('user', 'post', 'get_post_link', 'conteudo')
        }),
        ('Hierarquia', {
            'fields': ('parent', 'get_parent_link', 'get_replies_count')
        }),
        ('Status', {
            'fields': ('aprovado', 'ativo')
        }),
        ('Datas', {
            'fields': ('data_criacao', 'data_atualizacao'),
            'classes': ('collapse',)
        })
    )
    
    actions = ['aprovar_comentarios', 'reprovar_comentarios', 'desativar_comentarios']
    
    def get_usuario(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_usuario.short_description = 'Usuário'
    get_usuario.admin_order_field = 'user__username'
    
    def get_post_titulo(self, obj):
        if len(obj.post.titulo) > 30:
            return obj.post.titulo[:30] + '...'
        return obj.post.titulo
    get_post_titulo.short_description = 'Post'
    get_post_titulo.admin_order_field = 'post__titulo'
    
    def get_conteudo_resumido(self, obj):
        if len(obj.conteudo) > 50:
            return obj.conteudo[:50] + '...'
        return obj.conteudo
    get_conteudo_resumido.short_description = 'Conteúdo'
    
    def get_parent_info(self, obj):
        if obj.parent:
            return f'Resposta a #{obj.parent.id}'
        return 'Comentário principal'
    get_parent_info.short_description = 'Tipo'
    
    def get_post_link(self, obj):
        url = reverse('admin:alerts_post_change', args=[obj.post.id])
        return format_html('<a href="{}">Ver Post</a>', url)
    get_post_link.short_description = 'Link do Post'
    
    def get_parent_link(self, obj):
        if obj.parent:
            url = reverse('admin:alerts_comment_change', args=[obj.parent.id])
            return format_html('<a href="{}">Ver Comentário Pai</a>', url)
        return 'Nenhum'
    get_parent_link.short_description = 'Comentário Pai'
    
    def get_replies_count(self, obj):
        return obj.get_replies_count()
    get_replies_count.short_description = 'Respostas'
    
    def aprovar_comentarios(self, request, queryset):
        updated = queryset.update(aprovado=True)
        self.message_user(request, f'{updated} comentário(s) aprovado(s).')
    aprovar_comentarios.short_description = 'Aprovar comentários selecionados'
    
    def reprovar_comentarios(self, request, queryset):
        updated = queryset.update(aprovado=False)
        self.message_user(request, f'{updated} comentário(s) reprovado(s).')
    reprovar_comentarios.short_description = 'Reprovar comentários selecionados'
    
    def desativar_comentarios(self, request, queryset):
        updated = queryset.update(ativo=False)
        self.message_user(request, f'{updated} comentário(s) desativado(s).')
    desativar_comentarios.short_description = 'Desativar comentários selecionados'
