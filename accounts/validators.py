"""
Validators modulares para o app accounts
"""

import re
from datetime import date
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def validate_cpf(cpf):
    """
    Valida CPF brasileiro seguindo o algoritmo oficial

    Args:
        cpf (str): CPF a ser validado

    Raises:
        ValidationError: Se o CPF for inválido
    """
    if not cpf:
        raise ValidationError("CPF é obrigatório.")

    cpf_clean = re.sub(r"[^0-9]", "", str(cpf))

    if len(cpf_clean) != 11:
        raise ValidationError("CPF deve ter 11 dígitos.")

    if cpf_clean == cpf_clean[0] * 11:
        raise ValidationError("CPF inválido.")

    soma = sum(int(cpf_clean[i]) * (10 - i) for i in range(9))
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto

    soma = sum(int(cpf_clean[i]) * (11 - i) for i in range(10))
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto

    if int(cpf_clean[9]) != digito1 or int(cpf_clean[10]) != digito2:
        raise ValidationError("CPF inválido.")


def validate_phone_number(phone):
    """
    Valida número de telefone brasileiro

    Args:
        phone (str): Telefone a ser validado

    Raises:
        ValidationError: Se o telefone for inválido
    """
    if not phone:
        return

    phone_clean = re.sub(r"[^0-9]", "", str(phone))

    if len(phone_clean) < 10 or len(phone_clean) > 11:
        raise ValidationError("Telefone deve ter 10 ou 11 dígitos (com DDD).")

    ddd = int(phone_clean[:2])
    if ddd < 11 or ddd > 99:
        raise ValidationError("DDD inválido.")

    if len(phone_clean) == 11 and phone_clean[2] != "9":
        raise ValidationError("Para celular, o terceiro dígito deve ser 9.")


def validate_cep(cep):
    """
    Valida CEP brasileiro

    Args:
        cep (str): CEP a ser validado

    Raises:
        ValidationError: Se o CEP for inválido
    """
    if not cep:
        return

    cep_clean = re.sub(r"[^0-9]", "", str(cep))

    if len(cep_clean) != 8:
        raise ValidationError("CEP deve ter 8 dígitos.")

    if cep_clean == "00000000":
        raise ValidationError("CEP inválido.")


def validate_birth_date(birth_date):
    """
    Valida data de nascimento

    Args:
        birth_date (date): Data de nascimento a ser validada

    Raises:
        ValidationError: Se a data for inválida
    """
    if not birth_date:
        raise ValidationError("Data de nascimento é obrigatória.")

    today = date.today()

    if birth_date > today:
        raise ValidationError("Data de nascimento não pode ser futura.")

    age = (
        today.year
        - birth_date.year
        - ((today.month, today.day) < (birth_date.month, birth_date.day))
    )

    if age < 16:
        raise ValidationError("Contribuinte deve ter pelo menos 16 anos.")

    if age > 120:
        raise ValidationError("Data de nascimento inválida.")


def validate_florianopolis_neighborhood(neighborhood):
    """
    Valida se o bairro pertence a Florianópolis

    Args:
        neighborhood (str): Nome do bairro

    Raises:
        ValidationError: Se o bairro não for de Florianópolis
    """
    if not neighborhood:
        return

    FLORIANOPOLIS_NEIGHBORHOODS = [
        "Centro",
        "Trindade",
        "Pantanal",
        "Córrego Grande",
        "Santa Mônica",
        "Carvoeira",
        "Serrinha",
        "João Paulo",
        "Monte Verde",
        "Saco Grande",
        "Itacorubi",
        "Agronômica",
        "Capoeiras",
        "Coqueiros",
        "Estreito",
        "Balneário",
        "Coloninha",
        "Abraão",
        "Bom Abrigo",
        "Canto",
        "Canasvieiras",
        "Ingleses",
        "Santinho",
        "Cachoeira do Bom Jesus",
        "Ponta das Canas",
        "Lagoinha",
        "Daniela",
        "Jurerê",
        "Jurerê Internacional",
        "Praia Brava",
        "Barra da Lagoa",
        "Galheta",
        "Mole",
        "Joaquina",
        "Campeche",
        "Armação",
        "Matadeiro",
        "Lagoinha do Leste",
        "Pântano do Sul",
        "Costa de Dentro",
        "Ribeirão da Ilha",
        "Tapera",
        "Caieira da Barra do Sul",
        "Alto Ribeirão",
        "Sede Fragas",
        "Costeira do Pirajubaé",
        "Saco dos Limões",
        "José Mendes",
        "Prainha",
        "Bom Retiro",
        "Jardim Atlântico",
        "Vargem do Bom Jesus",
        "Vargem Grande",
        "Vargem Pequena",
        "Santo Antônio de Lisboa",
        "Ratones",
        "Cacupé",
        "Sambaqui",
        "Barra do Sambaqui",
        "Monte Cristo",
    ]

    neighborhood_normalized = neighborhood.strip().title()

    found = False
    for valid_neighborhood in FLORIANOPOLIS_NEIGHBORHOODS:
        if (
            neighborhood_normalized.lower() in valid_neighborhood.lower()
            or valid_neighborhood.lower() in neighborhood_normalized.lower()
        ):
            found = True
            break

    if not found:
        raise ValidationError(
            f'Bairro "{neighborhood}" não encontrado em Florianópolis. '
            "Verifique a grafia ou entre em contato com o suporte."
        )


phone_validator = RegexValidator(
    regex=r"^\(\d{2}\)\s\d{4,5}-\d{4}$",
    message="Telefone deve estar no formato: (48) 99999-9999",
    code="invalid_phone_format",
)

cep_validator = RegexValidator(
    regex=r"^\d{5}-?\d{3}$",
    message="CEP deve estar no formato: 88000-000",
    code="invalid_cep_format",
)


def format_cpf(cpf):
    """
    Formata CPF para exibição (XXX.XXX.XXX-XX)

    Args:
        cpf (str): CPF sem formatação

    Returns:
        str: CPF formatado
    """
    if not cpf:
        return cpf

    cpf_clean = re.sub(r"[^0-9]", "", str(cpf))
    if len(cpf_clean) == 11:
        return f"{cpf_clean[:3]}.{cpf_clean[3:6]}.{cpf_clean[6:9]}-{cpf_clean[9:]}"
    return cpf


def format_phone(phone):
    """
    Formata telefone para exibição

    Args:
        phone (str): Telefone sem formatação

    Returns:
        str: Telefone formatado
    """
    if not phone:
        return phone

    phone_clean = re.sub(r"[^0-9]", "", str(phone))

    if len(phone_clean) == 10:
        return f"({phone_clean[:2]}) {phone_clean[2:6]}-{phone_clean[6:]}"
    elif len(phone_clean) == 11:
        return f"({phone_clean[:2]}) {phone_clean[2:7]}-{phone_clean[7:]}"

    return phone


def format_cep(cep):
    """
    Formata CEP para exibição (XXXXX-XXX)

    Args:
        cep (str): CEP sem formatação

    Returns:
        str: CEP formatado
    """
    if not cep:
        return cep

    cep_clean = re.sub(r"[^0-9]", "", str(cep))
    if len(cep_clean) == 8:
        return f"{cep_clean[:5]}-{cep_clean[5:]}"
    return cep
