"""
Documentação Swagger/OpenAPI simplificada para rotas
"""

from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiParameter,
)
from drf_spectacular.openapi import OpenApiTypes

USER_CREATE_SIMPLE_SCHEMA = extend_schema(
    operation_id="user_create_simple",
    summary="Registrar novo usuário",
    description="Cria um novo usuário com perfil de contribuinte",
    tags=["Autenticação"],
    responses={
        201: OpenApiResponse(description="Usuário criado com sucesso"),
        400: OpenApiResponse(description="Dados inválidos"),
    },
)

USER_AVAILABILITY_SIMPLE_SCHEMA = extend_schema(
    operation_id="user_availability_simple",
    summary="Verificar disponibilidade",
    description="Verifica se username e email estão disponíveis",
    tags=["Autenticação"],
    parameters=[
        OpenApiParameter(
            name="username",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Nome de usuário a verificar",
            required=False,
        ),
        OpenApiParameter(
            name="email",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Email a verificar",
            required=False,
        ),
    ],
    responses={200: OpenApiResponse(description="Verificação realizada com sucesso")},
)

USER_PROFILE_SIMPLE_SCHEMA = extend_schema(
    operation_id="user_profile_simple",
    summary="Obter dados do usuário",
    description="Retorna informações do usuário e perfil",
    tags=["Perfil"],
    responses={
        200: OpenApiResponse(description="Dados obtidos com sucesso"),
        401: OpenApiResponse(description="Não autenticado"),
    },
)

PROFILE_UPDATE_SIMPLE_SCHEMA = extend_schema(
    operation_id="profile_update_simple",
    summary="Atualizar perfil",
    description="Atualiza informações do perfil",
    tags=["Perfil"],
    responses={
        200: OpenApiResponse(description="Perfil atualizado com sucesso"),
        400: OpenApiResponse(description="Dados inválidos"),
        401: OpenApiResponse(description="Não autenticado"),
    },
)

PROFILES_LIST_SIMPLE_SCHEMA = extend_schema(
    operation_id="profiles_list_simple",
    summary="Listar contribuintes",
    description="Lista contribuintes com filtros e paginação",
    tags=["Administração"],
    parameters=[
        OpenApiParameter(
            name="bairro",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Filtrar por bairro",
            required=False,
        ),
        OpenApiParameter(
            name="ativo",
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description="Filtrar por status ativo",
            required=False,
        ),
        OpenApiParameter(
            name="search",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Buscar por nome ou CPF",
            required=False,
        ),
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
            description="Itens por página",
            required=False,
        ),
    ],
    responses={
        200: OpenApiResponse(description="Lista obtida com sucesso"),
        401: OpenApiResponse(description="Não autenticado"),
        403: OpenApiResponse(description="Sem permissão"),
    },
)

STATS_SIMPLE_SCHEMA = extend_schema(
    operation_id="stats_simple",
    summary="Estatísticas do sistema",
    description="Retorna estatísticas de usuários e contribuintes",
    tags=["Administração"],
    responses={
        200: OpenApiResponse(description="Estatísticas geradas com sucesso"),
        401: OpenApiResponse(description="Não autenticado"),
        403: OpenApiResponse(description="Sem permissão"),
    },
)

CPF_VALIDATION_SIMPLE_SCHEMA = extend_schema(
    operation_id="cpf_validation_simple",
    summary="Validar CPF",
    description="Verifica se CPF é válido e disponível",
    tags=["Validação"],
    parameters=[
        OpenApiParameter(
            name="cpf",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="CPF a ser validado",
            required=True,
        )
    ],
    responses={
        200: OpenApiResponse(description="CPF validado com sucesso"),
        400: OpenApiResponse(description="CPF inválido"),
    },
)

PHONE_VALIDATION_SIMPLE_SCHEMA = extend_schema(
    operation_id="phone_validation_simple",
    summary="Validar telefone",
    description="Valida formato de telefone brasileiro",
    tags=["Validação"],
    parameters=[
        OpenApiParameter(
            name="phone",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Telefone a ser validado",
            required=True,
        )
    ],
    responses={
        200: OpenApiResponse(description="Telefone válido"),
        400: OpenApiResponse(description="Telefone inválido"),
    },
)

CEP_VALIDATION_SIMPLE_SCHEMA = extend_schema(
    operation_id="cep_validation_simple",
    summary="Validar CEP",
    description="Valida formato de CEP brasileiro",
    tags=["Validação"],
    parameters=[
        OpenApiParameter(
            name="cep",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="CEP a ser validado",
            required=True,
        )
    ],
    responses={
        200: OpenApiResponse(description="CEP válido"),
        400: OpenApiResponse(description="CEP inválido"),
    },
)

NEIGHBORHOODS_SIMPLE_SCHEMA = extend_schema(
    operation_id="neighborhoods_simple",
    summary="Listar bairros",
    description="Lista bairros de Florianópolis",
    tags=["Validação"],
    responses={200: OpenApiResponse(description="Lista de bairros obtida com sucesso")},
)
