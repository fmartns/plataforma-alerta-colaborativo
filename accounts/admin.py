from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from .models import Profile


class ProfileInline(admin.StackedInline):
    """
    Inline para exibir o perfil junto com o usuário
    """

    model = Profile
    can_delete = False
    verbose_name_plural = "Perfil do Contribuinte"
    fields = (
        "cpf",
        "foto",
        "data_nascimento",
        "telefone",
        "endereco",
        "bairro",
        "cep",
        "ativo",
    )


class CustomUserAdmin(UserAdmin):
    """
    Admin customizado para User incluindo o perfil
    """

    inlines = (ProfileInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Admin para gerenciar perfis dos contribuintes
    """

    list_display = (
        "get_nome_completo",
        "get_cpf_formatado",
        "get_idade_display",
        "bairro",
        "ativo",
        "data_cadastro",
    )

    list_filter = ("ativo", "bairro", "data_cadastro", "data_nascimento")

    search_fields = (
        "user__first_name",
        "user__last_name",
        "user__username",
        "cpf",
        "telefone",
        "bairro",
        "endereco",
    )

    readonly_fields = (
        "data_cadastro",
        "data_atualizacao",
        "get_cpf_formatado",
        "get_telefone_formatado",
        "get_cep_formatado",
        "get_idade_display",
        "get_foto_preview",
    )

    fieldsets = (
        ("Informações do Usuário", {"fields": ("user",)}),
        ("Documentos", {"fields": ("cpf", "get_cpf_formatado")}),
        (
            "Informações Pessoais",
            {
                "fields": (
                    "foto",
                    "get_foto_preview",
                    "data_nascimento",
                    "get_idade_display",
                    "telefone",
                    "get_telefone_formatado",
                )
            },
        ),
        ("Endereço", {"fields": ("endereco", "bairro", "cep", "get_cep_formatado")}),
        ("Status", {"fields": ("ativo",)}),
        (
            "Datas",
            {"fields": ("data_cadastro", "data_atualizacao"), "classes": ("collapse",)},
        ),
    )

    def get_nome_completo(self, obj):
        """Retorna o nome completo do usuário"""
        return obj.user.get_full_name() or obj.user.username

    get_nome_completo.short_description = "Nome Completo"
    get_nome_completo.admin_order_field = "user__first_name"

    def get_idade_display(self, obj):
        """Exibe a idade calculada"""
        return f"{obj.get_idade()} anos"

    get_idade_display.short_description = "Idade"

    def get_foto_preview(self, obj):
        """Exibe preview da foto no admin"""
        if obj.foto:
            return format_html(
                '<img src="{}" style="max-width: 150px; max-height: 150px;" />',
                obj.foto.url,
            )
        return "Sem foto"

    get_foto_preview.short_description = "Preview da Foto"

    def save_model(self, request, obj, form, change):
        """Customiza o salvamento do modelo"""
        super().save_model(request, obj, form, change)

        if change:
            self.message_user(
                request,
                f"Perfil de {obj.user.get_full_name() or obj.user.username} atualizado com sucesso.",
            )
        else:
            self.message_user(
                request,
                f"Perfil de {obj.user.get_full_name() or obj.user.username} criado com sucesso.",
            )


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
