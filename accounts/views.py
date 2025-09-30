from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Profile


@login_required
def profile_view(request):
    """
    View para exibir o perfil do usuário logado
    """
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = None

    context = {"profile": profile, "user": request.user}
    return render(request, "accounts/profile.html", context)


def check_cpf_availability(request):
    """
    API endpoint para verificar se um CPF já está em uso
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
                }
            )

    return JsonResponse({"error": "CPF não fornecido"}, status=400)
