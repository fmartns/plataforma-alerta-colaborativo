"""
Documentação Swagger/OpenAPI para rotas de perfil
"""

from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse
from drf_spectacular.openapi import OpenApiTypes

USER_PROFILE_RESPONSE_EXAMPLE = OpenApiExample(
    "Perfil Completo",
    summary="Dados completos do usuário com perfil",
    description="Resposta com todas as informações do usuário e perfil",
    value={
        "id": 123,
        "username": "joao_silva",
        "email": "joao.silva@email.com",
        "first_name": "João",
        "last_name": "Silva",
        "is_active": True,
        "date_joined": "2025-09-29T10:30:00Z",
        "last_login": "2025-09-29T15:45:00Z",
        "profile": {
            "id": 456,
            "cpf": "12345678901",
            "cpf_formatado": "123.456.789-01",
            "foto": "http://localhost:8000/media/profiles/joao_silva/foto.jpg",
            "data_nascimento": "1990-05-15",
            "telefone": "48999887766",
            "telefone_formatado": "(48) 99988-7766",
            "endereco": "Rua das Flores, 123, Apto 45",
            "bairro": "Centro",
            "cep": "88010000",
            "cep_formatado": "88010-000",
            "ativo": True,
            "idade": 35,
            "data_cadastro": "2025-09-29T10:30:00Z",
            "data_atualizacao": "2025-09-29T15:45:00Z",
        },
    },
    response_only=True,
)

USER_WITHOUT_PROFILE_EXAMPLE = OpenApiExample(
    "Usuário Sem Perfil",
    summary="Usuário que ainda não tem perfil",
    description="Resposta quando o usuário não possui perfil cadastrado",
    value={
        "id": 789,
        "username": "usuario_novo",
        "email": "novo@email.com",
        "first_name": "Novo",
        "last_name": "Usuário",
        "is_active": True,
        "date_joined": "2025-09-29T16:00:00Z",
        "last_login": None,
        "profile": None,
    },
    response_only=True,
)

USER_UPDATE_REQUEST_EXAMPLE = OpenApiExample(
    "Atualizar Dados Básicos",
    summary="Atualização de nome e email",
    description="Exemplo de atualização dos dados básicos do usuário",
    value={
        "first_name": "João Carlos",
        "last_name": "Silva Santos",
        "email": "joao.carlos@novoemail.com",
    },
    request_only=True,
)

USER_UPDATE_SUCCESS_RESPONSE = OpenApiExample(
    "Atualização Bem-sucedida",
    summary="Dados atualizados com sucesso",
    description="Resposta após atualização bem-sucedida",
    value={
        "message": "Dados atualizados com sucesso",
        "user": {
            "first_name": "João Carlos",
            "last_name": "Silva Santos",
            "email": "joao.carlos@novoemail.com",
        },
    },
    response_only=True,
)

PROFILE_DETAIL_RESPONSE_EXAMPLE = OpenApiExample(
    "Perfil Detalhado",
    summary="Informações detalhadas do perfil",
    description="Dados completos do perfil do contribuinte",
    value={
        "id": 456,
        "cpf": "12345678901",
        "cpf_formatado": "123.456.789-01",
        "foto": "http://localhost:8000/media/profiles/joao_silva/foto.jpg",
        "data_nascimento": "1990-05-15",
        "telefone": "48999887766",
        "telefone_formatado": "(48) 99988-7766",
        "endereco": "Rua das Flores, 123, Apto 45",
        "bairro": "Centro",
        "cep": "88010000",
        "cep_formatado": "88010-000",
        "idade": 35,
    },
    response_only=True,
)

PROFILE_UPDATE_REQUEST_EXAMPLE = OpenApiExample(
    "Atualizar Perfil",
    summary="Atualização parcial do perfil",
    description="Exemplo de atualização de alguns campos do perfil",
    value={
        "telefone": "48988776655",
        "endereco": "Rua Nova, 456, Casa 2",
        "bairro": "Trindade",
        "cep": "88040000",
    },
    request_only=True,
)

PROFILE_UPDATE_SUCCESS_RESPONSE = OpenApiExample(
    "Perfil Atualizado",
    summary="Perfil atualizado com sucesso",
    description="Resposta após atualização do perfil",
    value={
        "message": "Perfil atualizado com sucesso",
        "profile": {
            "id": 456,
            "cpf": "12345678901",
            "cpf_formatado": "123.456.789-01",
            "telefone": "48988776655",
            "telefone_formatado": "(48) 98877-6655",
            "endereco": "Rua Nova, 456, Casa 2",
            "bairro": "Trindade",
            "cep": "88040000",
            "cep_formatado": "88040-000",
            "idade": 35,
        },
    },
    response_only=True,
)

USER_PROFILE_GET_SCHEMA = extend_schema(
    operation_id="user_profile_get",
    summary="Obter dados do usuário logado",
    description="""
    Retorna informações completas do usuário autenticado, incluindo seu perfil.

    **Autenticação Obrigatória:**
    - Header: `Authorization: Bearer <access_token>`

    **Resposta Inclui:**
    - Dados básicos do usuário (username, email, nome)
    - Status da conta (ativo, datas)
    - Perfil completo do contribuinte (se existir)
    - Campos formatados (CPF, telefone, CEP)
    - Campos calculados (idade)

    **Casos Especiais:**
    - Se o usuário não tem perfil: `profile` será `null`
    - Campos opcionais podem estar vazios
    - Foto retorna URL completa se existir
    """,
    tags=["Perfil do Usuário"],
    responses={
        200: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Dados do usuário obtidos com sucesso",
            examples=[USER_PROFILE_RESPONSE_EXAMPLE, USER_WITHOUT_PROFILE_EXAMPLE],
        ),
        401: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Token inválido ou expirado",
            examples=[
                OpenApiExample(
                    "Não Autenticado",
                    value={"detail": "Given token not valid for any token type"},
                )
            ],
        ),
        500: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Erro interno do servidor",
            examples=[
                OpenApiExample(
                    "Erro Interno",
                    value={
                        "message": "Erro ao obter dados do usuário",
                        "error": "Detalhes do erro",
                    },
                )
            ],
        ),
    },
)

USER_PROFILE_PATCH_SCHEMA = extend_schema(
    operation_id="user_profile_patch",
    summary="Atualizar dados básicos do usuário",
    description="""
    Atualiza informações básicas do usuário autenticado (não inclui perfil).

    **Campos Atualizáveis:**
    - `first_name`: Primeiro nome
    - `last_name`: Sobrenome
    - `email`: Email (deve ser único)

    **Validações:**
    - Email deve ser único no sistema
    - Campos opcionais podem ser omitidos
    - Atualização parcial suportada

    **Não Atualiza:**
    - Username (imutável)
    - Senha (use endpoint específico)
    - Dados do perfil (use `/me/profile/`)
    """,
    tags=["Perfil do Usuário"],
    examples=[USER_UPDATE_REQUEST_EXAMPLE],
    responses={
        200: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Dados atualizados com sucesso",
            examples=[USER_UPDATE_SUCCESS_RESPONSE],
        ),
        400: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Dados inválidos",
            examples=[
                OpenApiExample(
                    "Email Duplicado",
                    value={
                        "message": "Dados inválidos",
                        "errors": {"email": ["Este email já está em uso."]},
                    },
                )
            ],
        ),
        401: OpenApiResponse(
            response=OpenApiTypes.OBJECT, description="Não autenticado"
        ),
        500: OpenApiResponse(
            response=OpenApiTypes.OBJECT, description="Erro interno do servidor"
        ),
    },
)

USER_PROFILE_PUT_SCHEMA = extend_schema(
    operation_id="user_profile_put",
    summary="Atualizar dados completos do usuário",
    description="""
    Atualização completa dos dados básicos do usuário.

    **Diferença do PATCH:**
    - PUT: Todos os campos devem ser fornecidos
    - PATCH: Apenas campos a serem alterados

    **Campos Obrigatórios:**
    - `first_name`: Primeiro nome
    - `last_name`: Sobrenome
    - `email`: Email único
    """,
    tags=["Perfil do Usuário"],
    examples=[
        OpenApiExample(
            "Atualização Completa",
            value={
                "first_name": "João Carlos",
                "last_name": "Silva Santos",
                "email": "joao.carlos@email.com",
            },
            request_only=True,
        )
    ],
    responses={
        200: OpenApiResponse(
            response=OpenApiTypes.OBJECT, description="Dados atualizados com sucesso"
        ),
        400: OpenApiResponse(
            response=OpenApiTypes.OBJECT, description="Dados inválidos ou incompletos"
        ),
        401: OpenApiResponse(
            response=OpenApiTypes.OBJECT, description="Não autenticado"
        ),
    },
)

PROFILE_GET_SCHEMA = extend_schema(
    operation_id="profile_get",
    summary="Obter perfil do contribuinte",
    description="""
    Retorna informações detalhadas do perfil do contribuinte autenticado.

    **Inclui:**
    - Dados pessoais (CPF, data nascimento, telefone)
    - Endereço completo (endereço, bairro, CEP)
    - Campos formatados automaticamente
    - Idade calculada dinamicamente
    - Status ativo/inativo
    - Timestamps de criação e atualização

    **Formatação Automática:**
    - CPF: XXX.XXX.XXX-XX
    - Telefone: (XX) XXXXX-XXXX ou (XX) XXXX-XXXX
    - CEP: XXXXX-XXX
    """,
    tags=["Perfil do Contribuinte"],
    responses={
        200: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Perfil obtido com sucesso",
            examples=[PROFILE_DETAIL_RESPONSE_EXAMPLE],
        ),
        401: OpenApiResponse(
            response=OpenApiTypes.OBJECT, description="Não autenticado"
        ),
        404: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Perfil não encontrado",
            examples=[
                OpenApiExample("Perfil Não Encontrado", value={"detail": "Not found."})
            ],
        ),
    },
)

PROFILE_PATCH_SCHEMA = extend_schema(
    operation_id="profile_patch",
    summary="Atualizar perfil do contribuinte",
    description="""
    Atualiza informações do perfil do contribuinte (CPF não pode ser alterado).

    **Campos Atualizáveis:**
    - `foto`: Upload de nova foto de perfil
    - `data_nascimento`: Data de nascimento (mín. 16 anos)
    - `telefone`: Telefone brasileiro (10 ou 11 dígitos)
    - `endereco`: Endereço completo
    - `bairro`: Bairro de Florianópolis
    - `cep`: CEP brasileiro (8 dígitos)

    **Campos Protegidos:**
    - `cpf`: Não pode ser alterado após criação
    - `data_cadastro`: Timestamp automático
    - `data_atualizacao`: Atualizado automaticamente

    **Validações Automáticas:**
    - Telefone: Formato brasileiro com DDD válido
    - CEP: Formato brasileiro válido
    - Bairro: Deve ser de Florianópolis
    - Idade: Recalculada automaticamente
    """,
    tags=["Perfil do Contribuinte"],
    examples=[PROFILE_UPDATE_REQUEST_EXAMPLE],
    responses={
        200: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Perfil atualizado com sucesso",
            examples=[PROFILE_UPDATE_SUCCESS_RESPONSE],
        ),
        400: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Dados inválidos",
            examples=[
                OpenApiExample(
                    "Validação Falhou",
                    value={
                        "message": "Dados inválidos",
                        "errors": {
                            "telefone": [
                                "Telefone deve ter 10 ou 11 dígitos (com DDD)."
                            ],
                            "bairro": [
                                'Bairro "Inexistente" não encontrado em Florianópolis.'
                            ],
                        },
                    },
                )
            ],
        ),
        401: OpenApiResponse(
            response=OpenApiTypes.OBJECT, description="Não autenticado"
        ),
        404: OpenApiResponse(
            response=OpenApiTypes.OBJECT, description="Perfil não encontrado"
        ),
    },
)

PROFILE_PUT_SCHEMA = extend_schema(
    operation_id="profile_put",
    summary="Atualizar perfil completo",
    description="""
    Atualização completa do perfil do contribuinte (exceto CPF).

    **Diferença do PATCH:**
    - PUT: Todos os campos editáveis devem ser fornecidos
    - PATCH: Apenas campos a serem alterados

    **Campos Obrigatórios:**
    - `data_nascimento`: Data de nascimento

    **Campos Opcionais:**
    - `foto`, `telefone`, `endereco`, `bairro`, `cep`
    """,
    tags=["Perfil do Contribuinte"],
    examples=[
        OpenApiExample(
            "Atualização Completa do Perfil",
            value={
                "data_nascimento": "1990-05-15",
                "telefone": "48988776655",
                "endereco": "Rua Nova, 456, Casa 2",
                "bairro": "Trindade",
                "cep": "88040000",
            },
            request_only=True,
        )
    ],
    responses={
        200: OpenApiResponse(
            response=OpenApiTypes.OBJECT, description="Perfil atualizado com sucesso"
        ),
        400: OpenApiResponse(
            response=OpenApiTypes.OBJECT, description="Dados inválidos ou incompletos"
        ),
        401: OpenApiResponse(
            response=OpenApiTypes.OBJECT, description="Não autenticado"
        ),
        404: OpenApiResponse(
            response=OpenApiTypes.OBJECT, description="Perfil não encontrado"
        ),
    },
)

PROFILE_DELETE_SCHEMA = extend_schema(
    operation_id="profile_delete",
    summary="Desativar perfil",
    description="""
    Marca o perfil como inativo (soft delete).

    **Comportamento:**
    - Perfil não é excluído fisicamente
    - Campo `ativo` é marcado como `false`
    - Dados são preservados para auditoria
    - Usuário pode ser reativado por administradores

    **Efeitos:**
    - Perfil não aparece em listagens públicas
    - Funcionalidades podem ser limitadas
    - Histórico é mantido

    **Reversão:**
    - Apenas administradores podem reativar
    - Use endpoint `/profiles/inactive/` (admin)
    """,
    tags=["Perfil do Contribuinte"],
    responses={
        200: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Perfil desativado com sucesso",
            examples=[
                OpenApiExample(
                    "Perfil Desativado",
                    value={
                        "message": "Perfil desativado com sucesso",
                        "profile_id": 456,
                        "active": False,
                    },
                )
            ],
        ),
        401: OpenApiResponse(
            response=OpenApiTypes.OBJECT, description="Não autenticado"
        ),
        404: OpenApiResponse(
            response=OpenApiTypes.OBJECT, description="Perfil não encontrado"
        ),
        500: OpenApiResponse(
            response=OpenApiTypes.OBJECT, description="Erro ao desativar perfil"
        ),
    },
)
