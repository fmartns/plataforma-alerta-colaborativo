"""
Views legadas para compatibilidade com versões anteriores
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from ..models import Profile


@login_required
def profile_view(request):
    """
    View tradicional para exibir o perfil do usuário logado

    Esta view mantém compatibilidade com templates Django tradicionais.
    Para APIs REST, use UserProfileAPIView.
    """
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = None

    context = {
        "profile": profile,
        "user": request.user,
        "has_profile": profile is not None,
        "cpf_formatted": profile.get_cpf_formatado() if profile else None,
        "phone_formatted": profile.get_telefone_formatado() if profile else None,
        "cep_formatted": profile.get_cep_formatado() if profile else None,
        "age": profile.get_idade() if profile else None,
    }

    return render(request, "accounts/profile.html", context)


def check_cpf_availability(request):
    """
    View legada para verificar disponibilidade de CPF

    Esta view mantém compatibilidade com código anterior.
    Para APIs REST, use check_cpf_availability em validation.py.
    """
    if request.method == "GET":
        cpf = request.GET.get("cpf", "").strip()
        if cpf:
            import re

            cpf = re.sub(r"[^0-9]", "", cpf)

            exists = Profile.objects.filter(cpf=cpf).exists()
            return JsonResponse(
                {
                    "available": not exists,
                    "message": "CPF disponível" if not exists else "CPF já cadastrado",
                    "cpf": cpf,
                }
            )

    return JsonResponse({"error": "CPF não fornecido"}, status=400)


def user_profile_json(request):
    """
    View legada para retornar perfil em JSON

    Mantém compatibilidade com código JavaScript anterior.
    """
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Usuário não autenticado"}, status=401)

    try:
        profile = request.user.profile
        data = {
            "user": {
                "id": request.user.id,
                "username": request.user.username,
                "email": request.user.email,
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "full_name": request.user.get_full_name(),
            },
            "profile": {
                "id": profile.id,
                "cpf": profile.cpf,
                "cpf_formatted": profile.get_cpf_formatado(),
                "phone": profile.telefone,
                "phone_formatted": profile.get_telefone_formatado(),
                "address": profile.endereco,
                "neighborhood": profile.bairro,
                "cep": profile.cep,
                "cep_formatted": profile.get_cep_formatado(),
                "birth_date": (
                    profile.data_nascimento.isoformat()
                    if profile.data_nascimento
                    else None
                ),
                "age": profile.get_idade(),
                "active": profile.ativo,
                "photo_url": profile.foto.url if profile.foto else None,
                "created_at": profile.data_cadastro.isoformat(),
                "updated_at": profile.data_atualizacao.isoformat(),
            },
        }
        return JsonResponse(data)
    except Profile.DoesNotExist:
        return JsonResponse(
            {
                "user": {
                    "id": request.user.id,
                    "username": request.user.username,
                    "email": request.user.email,
                    "first_name": request.user.first_name,
                    "last_name": request.user.last_name,
                    "full_name": request.user.get_full_name(),
                },
                "profile": None,
                "has_profile": False,
            }
        )
