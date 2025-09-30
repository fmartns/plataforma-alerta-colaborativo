"""
Views para validação e utilitários
"""

from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from ..models import Profile
from ..docs.simple import (
    CPF_VALIDATION_SIMPLE_SCHEMA,
    PHONE_VALIDATION_SIMPLE_SCHEMA,
    CEP_VALIDATION_SIMPLE_SCHEMA,
    NEIGHBORHOODS_SIMPLE_SCHEMA,
)


@CPF_VALIDATION_SIMPLE_SCHEMA
@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def check_cpf_availability(request):
    """
    API endpoint para verificar se um CPF já está em uso

    Aceita CPF com ou sem formatação e retorna se está disponível para cadastro.
    """
    cpf = request.GET.get("cpf", "").strip()

    if not cpf:
        return Response(
            {"error": "CPF é obrigatório"}, status=status.HTTP_400_BAD_REQUEST
        )

    import re

    cpf_clean = re.sub(r"[^0-9]", "", cpf)

    if len(cpf_clean) != 11:
        return Response(
            {"error": "CPF deve ter 11 dígitos"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        from ..validators import validate_cpf

        validate_cpf(cpf_clean)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    exists = Profile.objects.filter(cpf=cpf_clean).exists()

    return Response(
        {
            "cpf": cpf_clean,
            "cpf_formatted": f"{cpf_clean[:3]}.{cpf_clean[3:6]}.{cpf_clean[6:9]}-{cpf_clean[9:]}",
            "available": not exists,
            "message": (
                "CPF disponível para cadastro"
                if not exists
                else "CPF já cadastrado no sistema"
            ),
        }
    )


@NEIGHBORHOODS_SIMPLE_SCHEMA
@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def list_neighborhoods(request):
    """
    API endpoint para listar bairros válidos de Florianópolis

    Retorna todos os bairros aceitos pelo sistema para validação.
    """
    neighborhoods = [
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

    return Response(
        {
            "neighborhoods": sorted(neighborhoods),
            "total": len(neighborhoods),
            "note": "Lista oficial de bairros de Florianópolis aceitos pelo sistema",
        }
    )


@PHONE_VALIDATION_SIMPLE_SCHEMA
@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def validate_phone(request):
    """
    API endpoint para validar telefone brasileiro
    """
    phone = request.GET.get("phone", "").strip()

    if not phone:
        return Response(
            {"error": "Telefone é obrigatório"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        from ..validators import validate_phone_number, format_phone

        validate_phone_number(phone)

        return Response(
            {
                "phone": phone,
                "phone_formatted": format_phone(phone),
                "valid": True,
                "message": "Telefone válido",
            }
        )
    except Exception as e:
        return Response(
            {"phone": phone, "valid": False, "error": str(e)},
            status=status.HTTP_400_BAD_REQUEST,
        )


@CEP_VALIDATION_SIMPLE_SCHEMA
@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def validate_cep(request):
    """
    API endpoint para validar CEP brasileiro
    """
    cep = request.GET.get("cep", "").strip()

    if not cep:
        return Response(
            {"error": "CEP é obrigatório"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        from ..validators import validate_cep, format_cep

        validate_cep(cep)

        return Response(
            {
                "cep": cep,
                "cep_formatted": format_cep(cep),
                "valid": True,
                "message": "CEP válido",
            }
        )
    except Exception as e:
        return Response(
            {"cep": cep, "valid": False, "error": str(e)},
            status=status.HTTP_400_BAD_REQUEST,
        )
