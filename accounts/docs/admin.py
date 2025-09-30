"""
Documentação Swagger/OpenAPI para rotas administrativas
"""

from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiResponse,
    OpenApiParameter,
)
from drf_spectacular.openapi import OpenApiTypes

PROFILES_LIST_RESPONSE_EXAMPLE = OpenApiExample(
    "Lista de Contribuintes",
    summary="Lista paginada de contribuintes ativos",
    description="Resposta com lista paginada de contribuintes",
    value={
        "count": 150,
        "next": "http://localhost:8000/accounts/profiles/?page=2&page_size=20",
        "previous": None,
        "page": 1,
        "page_size": 20,
        "total_pages": 8,
        "results": [
            {
                "id": 1,
                "user_name": "João Silva",
                "username": "joao_silva",
                "cpf_formatado": "123.456.789-01",
                "telefone_formatado": "(48) 99988-7766",
                "bairro": "Centro",
                "ativo": True,
                "idade": 35,
                "data_cadastro": "2025-09-29T10:30:00Z",
            },
            {
                "id": 2,
                "user_name": "Maria Santos",
                "username": "maria_santos",
                "cpf_formatado": "987.654.321-00",
                "telefone_formatado": "(48) 98877-6655",
                "bairro": "Trindade",
                "ativo": True,
                "idade": 28,
                "data_cadastro": "2025-09-28T14:15:00Z",
            },
        ],
    },
    response_only=True,
)

PROFILES_FILTERED_RESPONSE_EXAMPLE = OpenApiExample(
    "Lista Filtrada",
    summary="Resultado de busca filtrada",
    description="Lista filtrada por bairro e busca textual",
    value={
        "count": 25,
        "next": "http://localhost:8000/accounts/profiles/?page=2&bairro=Centro&search=João",
        "previous": None,
        "page": 1,
        "page_size": 20,
        "total_pages": 2,
        "results": [
            {
                "id": 1,
                "user_name": "João Silva",
                "username": "joao_silva",
                "cpf_formatado": "123.456.789-01",
                "telefone_formatado": "(48) 99988-7766",
                "bairro": "Centro",
                "ativo": True,
                "idade": 35,
                "data_cadastro": "2025-09-29T10:30:00Z",
            }
        ],
    },
    response_only=True,
)

STATS_RESPONSE_EXAMPLE = OpenApiExample(
    "Estatísticas Completas",
    summary="Dashboard completo de estatísticas",
    description="Todas as métricas do sistema",
    value={
        "total_users": 500,
        "total_profiles": 450,
        "active_profiles": 420,
        "inactive_profiles": 30,
        "completion_rate": 90.0,
        "top_neighborhoods": [
            {"bairro": "Centro", "count": 85},
            {"bairro": "Trindade", "count": 72},
            {"bairro": "Ingleses", "count": 45},
            {"bairro": "Canasvieiras", "count": 38},
            {"bairro": "Campeche", "count": 32},
        ],
        "monthly_registrations": [
            {"month": "2025-04", "count": 45},
            {"month": "2025-05", "count": 62},
            {"month": "2025-06", "count": 78},
            {"month": "2025-07", "count": 55},
            {"month": "2025-08", "count": 89},
            {"month": "2025-09", "count": 67},
        ],
        "age_distribution": {
            "16-25": 45,
            "26-35": 125,
            "36-45": 98,
            "46-55": 87,
            "56-65": 45,
            "65+": 20,
        },
        "generated_at": "2025-09-29T16:30:00Z",
    },
    response_only=True,
)

INACTIVE_PROFILES_RESPONSE_EXAMPLE = OpenApiExample(
    "Perfis Inativos",
    summary="Lista de contribuintes desativados",
    description="Lista paginada de perfis marcados como inativos",
    value={
        "count": 30,
        "page": 1,
        "page_size": 20,
        "total_pages": 2,
        "results": [
            {
                "id": 15,
                "user_name": "Carlos Oliveira",
                "username": "carlos_oliveira",
                "cpf_formatado": "111.222.333-44",
                "telefone_formatado": "(48) 97766-5544",
                "bairro": "Lagoa",
                "ativo": False,
                "idade": 42,
                "data_cadastro": "2025-08-15T09:20:00Z",
            }
        ],
    },
    response_only=True,
)

REACTIVATE_PROFILE_REQUEST_EXAMPLE = OpenApiExample(
    "Reativar Perfil",
    summary="Solicitação de reativação",
    description="Dados para reativar um contribuinte",
    value={"profile_id": 15},
    request_only=True,
)

REACTIVATE_PROFILE_SUCCESS_EXAMPLE = OpenApiExample(
    "Reativação Bem-sucedida",
    summary="Perfil reativado com sucesso",
    description="Resposta após reativação do contribuinte",
    value={
        "message": "Contribuinte reativado com sucesso",
        "profile": {
            "id": 15,
            "user_name": "Carlos Oliveira",
            "username": "carlos_oliveira",
            "cpf_formatado": "111.222.333-44",
            "telefone_formatado": "(48) 97766-5544",
            "bairro": "Lagoa",
            "ativo": True,
            "idade": 42,
            "data_cadastro": "2025-08-15T09:20:00Z",
        },
    },
    response_only=True,
)

PROFILES_LIST_GET_SCHEMA = extend_schema(
    operation_id="admin_profiles_list",
    summary="Listar contribuintes",
    description="""
    Lista contribuintes com filtros avançados e paginação (apenas administradores).

    **Permissões:**
    - Apenas usuários com `is_staff=True`
    - Header: `Authorization: Bearer <admin_access_token>`

    **Filtros Disponíveis:**
    - `bairro`: Filtrar por bairro específico
    - `ativo`: Filtrar por status (true/false)
    - `search`: Buscar por nome, username ou CPF
    - `page`: Número da página (padrão: 1)
    - `page_size`: Itens por página (padrão: 20, máximo: 100)

    **Ordenação:**
    - Por padrão: Data de cadastro (mais recentes primeiro)
    - Otimizado com `select_related('user')`

    **Paginação:**
    - URLs de navegação automáticas
    - Metadados completos (total, páginas, etc.)
    - Preserva parâmetros de filtro na navegação

    **Performance:**
    - Queries otimizadas
    - Limite de 100 itens por página
    - Cache-friendly
    """,
    tags=["Administração"],
    parameters=[
        OpenApiParameter(
            name="bairro",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Filtrar por bairro (busca parcial)",
            required=False,
            examples=[
                OpenApiExample("Centro", summary="Filtrar por Centro", value="Centro"),
                OpenApiExample(
                    "Trindade", summary="Filtrar por Trindade", value="Trindade"
                ),
                OpenApiExample(
                    "Ingleses", summary="Filtrar por Ingleses", value="Ingleses"
                ),
            ],
        ),
        OpenApiParameter(
            name="ativo",
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description="Filtrar por status ativo",
            required=False,
            examples=[
                OpenApiExample(
                    "Apenas Ativos", summary="Mostrar apenas ativos", value=True
                ),
                OpenApiExample(
                    "Apenas Inativos", summary="Mostrar apenas inativos", value=False
                ),
            ],
        ),
        OpenApiParameter(
            name="search",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Buscar por nome, username ou CPF",
            required=False,
            examples=[
                OpenApiExample("Por Nome", summary="Buscar por nome", value="João"),
                OpenApiExample("Por CPF", summary="Buscar por CPF", value="123456789"),
                OpenApiExample(
                    "Por Username", summary="Buscar por username", value="joao_silva"
                ),
            ],
        ),
        OpenApiParameter(
            name="page",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description="Número da página",
            required=False,
            examples=[
                OpenApiExample("Primeira Página", summary="Página inicial", value=1),
                OpenApiExample("Segunda Página", summary="Segunda página", value=2),
            ],
        ),
        OpenApiParameter(
            name="page_size",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description="Itens por página (máximo 100)",
            required=False,
            examples=[
                OpenApiExample("Padrão", summary="Tamanho padrão", value=20),
                OpenApiExample("Mais Itens", summary="Mais itens por página", value=50),
                OpenApiExample("Máximo", summary="Máximo permitido", value=100),
            ],
        ),
    ],
    responses={
        200: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Lista obtida com sucesso",
            examples=[
                PROFILES_LIST_RESPONSE_EXAMPLE,
                PROFILES_FILTERED_RESPONSE_EXAMPLE,
            ],
        ),
        401: OpenApiResponse(
            response=OpenApiTypes.OBJECT, description="Token inválido ou expirado"
        ),
        403: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Sem permissão de administrador",
            examples=[
                OpenApiExample(
                    "Acesso Negado",
                    value={
                        "detail": "You do not have permission to perform this action."
                    },
                )
            ],
        ),
        500: OpenApiResponse(
            response=OpenApiTypes.OBJECT, description="Erro interno do servidor"
        ),
    },
)

STATS_GET_SCHEMA = extend_schema(
    operation_id="admin_user_stats",
    summary="Estatísticas do sistema",
    description="""
    Retorna estatísticas completas dos usuários e contribuintes (apenas administradores).

    **Métricas Incluídas:**

    **📊 Básicas:**
    - Total de usuários registrados
    - Total de perfis criados
    - Perfis ativos vs inativos
    - Taxa de completude (perfis/usuários)

    **🏘️ Por Localização:**
    - Top 10 bairros com mais contribuintes
    - Distribuição geográfica

    **📅 Temporais:**
    - Registros mensais (últimos 6 meses)
    - Tendências de crescimento

    **👥 Demográficas:**
    - Distribuição por faixa etária
    - Análise de idades dos contribuintes

    **⚡ Performance:**
    - Cache-friendly para dashboards
    - Queries otimizadas
    - Cálculos em tempo real

    **🔄 Atualização:**
    - Timestamp de geração
    - Dados sempre atuais
    """,
    tags=["Administração"],
    responses={
        200: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Estatísticas geradas com sucesso",
            examples=[STATS_RESPONSE_EXAMPLE],
        ),
        401: OpenApiResponse(
            response=OpenApiTypes.OBJECT, description="Token inválido ou expirado"
        ),
        403: OpenApiResponse(
            response=OpenApiTypes.OBJECT, description="Sem permissão de administrador"
        ),
        500: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Erro ao gerar estatísticas",
            examples=[
                OpenApiExample(
                    "Erro de Cálculo",
                    value={
                        "message": "Erro ao gerar estatísticas",
                        "error": "Erro no cálculo de distribuição etária",
                    },
                )
            ],
        ),
    },
)

INACTIVE_PROFILES_GET_SCHEMA = extend_schema(
    operation_id="admin_inactive_profiles_list",
    summary="Listar contribuintes inativos",
    description="""
    Lista todos os contribuintes marcados como inativos (apenas administradores).

    **Finalidade:**
    - Gerenciar perfis desativados
    - Auditoria de desativações
    - Processo de reativação

    **Ordenação:**
    - Por data de atualização (mais recentes primeiro)
    - Mostra quando foram desativados

    **Paginação:**
    - Padrão: 20 itens por página
    - Máximo: 100 itens por página
    - Navegação simplificada

    **Dados Incluídos:**
    - Informações básicas do contribuinte
    - Data de cadastro original
    - Última atualização (desativação)
    - Dados formatados para exibição
    """,
    tags=["Administração"],
    parameters=[
        OpenApiParameter(
            name="page",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description="Número da página",
            required=False,
        ),
        OpenApiParameter(
            name="page_size",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description="Itens por página (máximo 100)",
            required=False,
        ),
    ],
    responses={
        200: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Lista de inativos obtida com sucesso",
            examples=[INACTIVE_PROFILES_RESPONSE_EXAMPLE],
        ),
        401: OpenApiResponse(
            response=OpenApiTypes.OBJECT, description="Token inválido ou expirado"
        ),
        403: OpenApiResponse(
            response=OpenApiTypes.OBJECT, description="Sem permissão de administrador"
        ),
        500: OpenApiResponse(
            response=OpenApiTypes.OBJECT, description="Erro ao listar perfis inativos"
        ),
    },
)

INACTIVE_PROFILES_PATCH_SCHEMA = extend_schema(
    operation_id="admin_reactivate_profile",
    summary="Reativar contribuinte",
    description="""
    Reativa um contribuinte que estava marcado como inativo (apenas administradores).

    **Processo:**
    1. Localiza o perfil pelo ID
    2. Verifica se está realmente inativo
    3. Marca como ativo (`ativo = True`)
    4. Registra log de auditoria
    5. Retorna dados atualizados

    **Validações:**
    - Perfil deve existir
    - Perfil deve estar inativo
    - ID deve ser fornecido

    **Auditoria:**
    - Log da reativação
    - Usuário administrador responsável
    - Timestamp da operação

    **Efeitos:**
    - Perfil volta a aparecer em listagens
    - Funcionalidades são restauradas
    - Histórico é preservado

    **Segurança:**
    - Apenas administradores
    - Log completo da operação
    - Validações rigorosas
    """,
    tags=["Administração"],
    examples=[REACTIVATE_PROFILE_REQUEST_EXAMPLE],
    responses={
        200: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Contribuinte reativado com sucesso",
            examples=[REACTIVATE_PROFILE_SUCCESS_EXAMPLE],
        ),
        400: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="ID do perfil não fornecido",
            examples=[
                OpenApiExample(
                    "ID Obrigatório", value={"message": "ID do perfil é obrigatório"}
                )
            ],
        ),
        401: OpenApiResponse(
            response=OpenApiTypes.OBJECT, description="Token inválido ou expirado"
        ),
        403: OpenApiResponse(
            response=OpenApiTypes.OBJECT, description="Sem permissão de administrador"
        ),
        404: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Perfil não encontrado ou já ativo",
            examples=[
                OpenApiExample(
                    "Perfil Não Encontrado",
                    value={"message": "Perfil não encontrado ou já está ativo"},
                )
            ],
        ),
        500: OpenApiResponse(
            response=OpenApiTypes.OBJECT, description="Erro ao reativar contribuinte"
        ),
    },
)
