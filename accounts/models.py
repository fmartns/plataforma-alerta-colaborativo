from django.db import models
from django.contrib.auth.models import User
import re
from .validators import (
    validate_cpf,
    validate_phone_number,
    validate_cep,
    validate_birth_date,
    validate_florianopolis_neighborhood,
    format_cpf,
    format_phone,
    format_cep,
)


def user_photo_path(instance, filename):
    """
    Define o caminho para upload das fotos de perfil
    """
    return f"profiles/{instance.user.username}/{filename}"


class Profile(models.Model):
    """
    Perfil do contribuinte de Florianópolis
    Estende o modelo User padrão do Django
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="Usuário", related_name="profile"
    )

    cpf = models.CharField(
        max_length=14,
        unique=True,
        validators=[validate_cpf],
        verbose_name="CPF",
        help_text="Digite apenas os números do CPF",
    )

    foto = models.ImageField(
        upload_to=user_photo_path,
        blank=True,
        null=True,
        verbose_name="Foto de Perfil",
        help_text="Foto do contribuinte",
    )

    data_nascimento = models.DateField(
        validators=[validate_birth_date],
        verbose_name="Data de Nascimento",
        help_text="Data de nascimento do contribuinte (mínimo 16 anos)",
    )

    telefone = models.CharField(
        max_length=15,
        blank=True,
        validators=[validate_phone_number],
        verbose_name="Telefone",
        help_text="Telefone de contato (formato: (48) 99999-9999)",
    )

    endereco = models.TextField(
        blank=True,
        verbose_name="Endereço",
        help_text="Endereço completo em Florianópolis",
    )

    bairro = models.CharField(
        max_length=100,
        blank=True,
        validators=[validate_florianopolis_neighborhood],
        verbose_name="Bairro",
        help_text="Bairro de residência em Florianópolis",
    )

    cep = models.CharField(
        max_length=9,
        blank=True,
        validators=[validate_cep],
        verbose_name="CEP",
        help_text="CEP do endereço (formato: 88000-000)",
    )

    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo",
        help_text="Indica se o contribuinte está ativo na plataforma",
    )

    data_cadastro = models.DateTimeField(
        auto_now_add=True, verbose_name="Data de Cadastro"
    )

    data_atualizacao = models.DateTimeField(
        auto_now=True, verbose_name="Última Atualização"
    )

    class Meta:
        verbose_name = "Perfil do Contribuinte"
        verbose_name_plural = "Perfis dos Contribuintes"
        ordering = ["-data_cadastro"]

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.cpf}"

    def clean(self):
        """
        Validações customizadas e formatação de campos
        """
        super().clean()

        if self.cpf:
            self.cpf = re.sub(r"[^0-9]", "", self.cpf)

        if self.telefone:
            self.telefone = re.sub(r"[^0-9]", "", self.telefone)

        if self.cep:
            self.cep = re.sub(r"[^0-9]", "", self.cep)

    def get_cpf_formatado(self):
        """
        Retorna o CPF formatado (XXX.XXX.XXX-XX)
        """
        return format_cpf(self.cpf)

    def get_telefone_formatado(self):
        """
        Retorna o telefone formatado
        """
        return format_phone(self.telefone)

    def get_cep_formatado(self):
        """
        Retorna o CEP formatado (XXXXX-XXX)
        """
        return format_cep(self.cep)

    def get_idade(self):
        """
        Calcula a idade do contribuinte
        """
        from datetime import date

        today = date.today()
        return (
            today.year
            - self.data_nascimento.year
            - (
                (today.month, today.day)
                < (self.data_nascimento.month, self.data_nascimento.day)
            )
        )
