"""
Serializers para modelo Profile
"""

from rest_framework import serializers
from ..models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer completo para o modelo Profile
    """

    cpf_formatado = serializers.CharField(source="get_cpf_formatado", read_only=True)
    telefone_formatado = serializers.CharField(
        source="get_telefone_formatado", read_only=True
    )
    cep_formatado = serializers.CharField(source="get_cep_formatado", read_only=True)
    idade = serializers.IntegerField(source="get_idade", read_only=True)

    class Meta:
        model = Profile
        fields = [
            "id",
            "cpf",
            "cpf_formatado",
            "foto",
            "data_nascimento",
            "telefone",
            "telefone_formatado",
            "endereco",
            "bairro",
            "cep",
            "cep_formatado",
            "ativo",
            "idade",
            "data_cadastro",
            "data_atualizacao",
        ]
        read_only_fields = ["data_cadastro", "data_atualizacao"]

    def validate_cpf(self, value):
        """
        Valida CPF único no sistema (exceto para o próprio usuário)
        """
        import re

        cpf_clean = re.sub(r"[^0-9]", "", str(value))

        queryset = Profile.objects.filter(cpf=cpf_clean)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError("Este CPF já está cadastrado.")

        return cpf_clean


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para atualização de perfil (CPF não pode ser alterado)
    """

    cpf_formatado = serializers.CharField(source="get_cpf_formatado", read_only=True)
    telefone_formatado = serializers.CharField(
        source="get_telefone_formatado", read_only=True
    )
    cep_formatado = serializers.CharField(source="get_cep_formatado", read_only=True)
    idade = serializers.IntegerField(source="get_idade", read_only=True)

    class Meta:
        model = Profile
        fields = [
            "cpf",
            "cpf_formatado",
            "foto",
            "data_nascimento",
            "telefone",
            "telefone_formatado",
            "endereco",
            "bairro",
            "cep",
            "cep_formatado",
            "idade",
        ]
        read_only_fields = ["cpf"]  # CPF não pode ser alterado após criação

    def validate(self, attrs):
        """
        Validações customizadas e formatação
        """
        import re

        if "telefone" in attrs and attrs["telefone"]:
            attrs["telefone"] = re.sub(r"[^0-9]", "", attrs["telefone"])

        if "cep" in attrs and attrs["cep"]:
            attrs["cep"] = re.sub(r"[^0-9]", "", attrs["cep"])

        return attrs


class ProfileListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listagem de perfis
    """

    user_name = serializers.CharField(source="user.get_full_name", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    cpf_formatado = serializers.CharField(source="get_cpf_formatado", read_only=True)
    telefone_formatado = serializers.CharField(
        source="get_telefone_formatado", read_only=True
    )
    idade = serializers.IntegerField(source="get_idade", read_only=True)

    class Meta:
        model = Profile
        fields = [
            "id",
            "user_name",
            "username",
            "cpf_formatado",
            "telefone_formatado",
            "bairro",
            "ativo",
            "idade",
            "data_cadastro",
        ]


class ProfileStatsSerializer(serializers.Serializer):
    """
    Serializer para estatísticas de perfis
    """

    total_users = serializers.IntegerField()
    total_profiles = serializers.IntegerField()
    active_profiles = serializers.IntegerField()
    inactive_profiles = serializers.IntegerField()
    top_neighborhoods = serializers.ListField(child=serializers.DictField())
