"""
Documentação Swagger/OpenAPI para rotas de autenticação
"""

from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiResponse,
    OpenApiParameter,
)
from drf_spectacular.openapi import OpenApiTypes

USER_REGISTER_REQUEST_EXAMPLE = OpenApiExample(
    "Registro Completo",
    summary="Exemplo de registro com todos os campos",
    description="Registro de um contribuinte com perfil completo",
    value={
        "username": "joao_silva",
        "email": "joao.silva@email.com",
        "first_name": "João",
        "last_name": "Silva",
        "password": "minhasenha123",
        "password_confirm": "minhasenha123",
        "profile": {
            "cpf": "12345678901",
            "data_nascimento": "1990-05-15",
            "telefone": "48999887766",
            "endereco": "Rua das Flores, 123, Apto 45",
            "bairro": "Centro",
            "cep": "88010000",
        },
    },
    request_only=True,
)

USER_REGISTER_MINIMAL_EXAMPLE = OpenApiExample(
    "Registro Mínimo",
    summary="Exemplo com campos obrigatórios apenas",
    description="Registro com apenas os campos essenciais",
    value={
        "username": "maria_santos",
        "email": "maria@email.com",
        "first_name": "Maria",
        "last_name": "Santos",
        "password": "senha123456",
        "password_confirm": "senha123456",
        "profile": {"cpf": "98765432100", "data_nascimento": "1985-12-03"},
    },
    request_only=True,
)

USER_REGISTER_SUCCESS_RESPONSE = OpenApiExample(
    "Sucesso",
    summary="Usuário criado com sucesso",
    description="Resposta quando o usuário é criado com sucesso",
    value={
        "message": "Usuário criado com sucesso",
        "user_id": 123,
        "username": "joao_silva",
        "profile_created": True,
        "cpf": "123.456.789-01",
    },
    response_only=True,
)

USER_REGISTER_ERROR_RESPONSE = OpenApiExample(
    "Erro de Validação",
    summary="Dados inválidos fornecidos",
    description="Resposta quando há erros de validação",
    value={
        "message": "Dados inválidos",
        "errors": {
            "username": ["Este nome de usuário já está em uso."],
            "email": ["Este email já está em uso."],
            "profile": {"cpf": ["Este CPF já está cadastrado."]},
        },
    },
    response_only=True,
)

AVAILABILITY_CHECK_EXAMPLE = OpenApiExample(
    "Verificação de Disponibilidade",
    summary="Verificar username e email",
    description="Verificar se username e email estão disponíveis",
    value={
        "username_available": True,
        "username": "novo_usuario",
        "email_available": False,
        "email": "email@existente.com",
    },
    response_only=True,
)

USER_CREATE_POST_SCHEMA = extend_schema(
    operation_id="user_create",
    summary="Registrar novo usuário",
    description="""
    Cria um novo usuário com perfil de contribuinte completo.

    **Campos Obrigatórios:**
    - `username`: Nome de usuário único (3-150 caracteres)
    - `email`: Email único e válido
    - `password`: Senha (mínimo 8 caracteres)
    - `password_confirm`: Confirmação da senha (deve ser igual à senha)
    - `first_name`: Primeiro nome
    - `last_name`: Sobrenome
    - `profile.cpf`: CPF válido e único (apenas números)
    - `profile.data_nascimento`: Data de nascimento (idade mínima: 16 anos)

    **Campos Opcionais do Perfil:**
    - `profile.foto`: Foto de perfil (upload de imagem)
    - `profile.telefone`: Telefone brasileiro (10 ou 11 dígitos)
    - `profile.endereco`: Endereço completo
    - `profile.bairro`: Bairro de Florianópolis
    - `profile.cep`: CEP brasileiro (8 dígitos)

    **Validações Automáticas:**
    - CPF: Validação algorítmica completa
    - Telefone: Formato brasileiro com DDD
    - CEP: Formato brasileiro
    - Bairro: Deve ser de Florianópolis
    - Idade: Mínimo 16 anos, máximo 120 anos
    """,
    tags=["Autenticação"],
    examples=[USER_REGISTER_REQUEST_EXAMPLE, USER_REGISTER_MINIMAL_EXAMPLE],
    responses={
        201: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Usuário criado com sucesso",
            examples=[USER_REGISTER_SUCCESS_RESPONSE],
        ),
        400: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Dados inválidos",
            examples=[USER_REGISTER_ERROR_RESPONSE],
        ),
        500: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Erro interno do servidor",
            examples=[
                OpenApiExample(
                    "Erro Interno",
                    value={
                        "message": "Erro interno do servidor",
                        "error": "Detalhes do erro",
                    },
                )
            ],
        ),
    },
)

USER_CREATE_GET_SCHEMA = extend_schema(
    operation_id="user_availability_check",
    summary="Verificar disponibilidade",
    description="""
    Verifica se username e/ou email estão disponíveis para registro.

    **Parâmetros de Query:**
    - `username`: Nome de usuário a verificar
    - `email`: Email a verificar

    **Uso:**
    - Pode verificar apenas username: `?username=novo_usuario`
    - Pode verificar apenas email: `?email=novo@email.com`
    - Pode verificar ambos: `?username=novo_usuario&email=novo@email.com`

    **Resposta:**
    - `username_available`: true se disponível, false se já existe
    - `email_available`: true se disponível, false se já existe
    """,
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
    responses={
        200: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Verificação realizada com sucesso",
            examples=[AVAILABILITY_CHECK_EXAMPLE],
        ),
        400: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Parâmetros inválidos",
            examples=[
                OpenApiExample(
                    "Parâmetros Obrigatórios",
                    value={
                        "message": "Forneça username ou email para verificar disponibilidade"
                    },
                )
            ],
        ),
    },
)

JWT_LOGIN_EXAMPLE = OpenApiExample(
    "Login",
    summary="Login com username e senha",
    description="Fazer login para obter tokens JWT",
    value={"username": "joao_silva", "password": "minhasenha123"},
    request_only=True,
)

JWT_SUCCESS_RESPONSE = OpenApiExample(
    "Login Bem-sucedido",
    summary="Tokens JWT retornados",
    description="Resposta com tokens de acesso e refresh",
    value={
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "username": "joao_silva",
        "email": "joao.silva@email.com",
        "first_name": "João",
        "last_name": "Silva",
        "has_profile": True,
        "cpf": "123.456.789-01",
        "ativo": True,
    },
    response_only=True,
)

JWT_ERROR_RESPONSE = OpenApiExample(
    "Credenciais Inválidas",
    summary="Login falhou",
    description="Resposta quando as credenciais estão incorretas",
    value={"detail": "No active account found with the given credentials"},
    response_only=True,
)

JWT_OBTAIN_SCHEMA = extend_schema(
    operation_id="jwt_obtain",
    summary="Fazer login (obter tokens)",
    description="""
    Autentica o usuário e retorna tokens JWT.

    **Como usar:**
    1. Envie username e password
    2. Receba access_token (válido por 60 minutos)
    3. Receba refresh_token (válido por 7 dias)
    4. Use o access_token no header: `Authorization: Bearer <access_token>`

    **Informações do Token:**
    - Access Token: Usado para autenticação nas APIs (60 min)
    - Refresh Token: Usado para renovar o access token (7 dias)
    - Tokens incluem informações do usuário e perfil
    """,
    tags=["JWT Authentication"],
    examples=[JWT_LOGIN_EXAMPLE],
    responses={
        200: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Login realizado com sucesso",
            examples=[JWT_SUCCESS_RESPONSE],
        ),
        401: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Credenciais inválidas",
            examples=[JWT_ERROR_RESPONSE],
        ),
    },
)

JWT_REFRESH_SCHEMA = extend_schema(
    operation_id="jwt_refresh",
    summary="Renovar token de acesso",
    description="""
    Renova o token de acesso usando o refresh token.

    **Como usar:**
    1. Envie o refresh_token
    2. Receba um novo access_token
    3. O refresh_token pode ser rotacionado (novo refresh_token)

    **Configurações:**
    - Rotação de refresh tokens habilitada
    - Blacklist de tokens antigos habilitada
    """,
    tags=["JWT Authentication"],
    examples=[
        OpenApiExample(
            "Renovar Token",
            value={"refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."},
            request_only=True,
        )
    ],
    responses={
        200: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Token renovado com sucesso",
            examples=[
                OpenApiExample(
                    "Token Renovado",
                    value={
                        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                    },
                )
            ],
        ),
        401: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Refresh token inválido",
            examples=[
                OpenApiExample(
                    "Token Inválido",
                    value={
                        "detail": "Token is invalid or expired",
                        "code": "token_not_valid",
                    },
                )
            ],
        ),
    },
)

JWT_VERIFY_SCHEMA = extend_schema(
    operation_id="jwt_verify",
    summary="Verificar validade do token",
    description="""
    Verifica se um token JWT é válido.

    **Como usar:**
    1. Envie o token (access ou refresh)
    2. Receba confirmação de validade

    **Útil para:**
    - Verificar se token expirou
    - Validar tokens antes de usar
    - Debug de problemas de autenticação
    """,
    tags=["JWT Authentication"],
    examples=[
        OpenApiExample(
            "Verificar Token",
            value={"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."},
            request_only=True,
        )
    ],
    responses={
        200: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Token válido",
            examples=[OpenApiExample("Token Válido", value={})],
        ),
        401: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Token inválido",
            examples=[
                OpenApiExample(
                    "Token Inválido",
                    value={
                        "detail": "Token is invalid or expired",
                        "code": "token_not_valid",
                    },
                )
            ],
        ),
    },
)
