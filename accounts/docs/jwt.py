"""
Documentação Swagger/OpenAPI para autenticação JWT
"""

from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse
from drf_spectacular.openapi import OpenApiTypes

JWT_TOKEN_OBTAIN_REQUEST_EXAMPLE = OpenApiExample(
    "Login Padrão",
    summary="Login com username e senha",
    description="Credenciais para obter tokens JWT",
    value={"username": "joao_silva", "password": "minhasenha123"},
    request_only=True,
)

JWT_TOKEN_OBTAIN_SUCCESS_EXAMPLE = OpenApiExample(
    "Login Bem-sucedido",
    summary="Tokens JWT retornados com dados do usuário",
    description="Resposta completa com tokens e informações do perfil",
    value={
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk1OTk5OTk5LCJpYXQiOjE2OTU5OTYzOTksImp0aSI6IjEyMzQ1Njc4OTAiLCJ1c2VyX2lkIjoxMjMsInVzZXJuYW1lIjoiam9hb19zaWx2YSIsImVtYWlsIjoiam9hby5zaWx2YUBlbWFpbC5jb20iLCJmaXJzdF9uYW1lIjoiSm9cdTAwZTNvIiwibGFzdF9uYW1lIjoiU2lsdmEiLCJoYXNfcHJvZmlsZSI6dHJ1ZSwiY3BmIjoiMTIzLjQ1Ni43ODktMDEiLCJhdGl2byI6dHJ1ZX0.signature",
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5NjYwMTM5OSwiaWF0IjoxNjk1OTk2Mzk5LCJqdGkiOiI5ODc2NTQzMjEwIiwidXNlcl9pZCI6MTIzfQ.signature",
        "token_type": "Bearer",
        "expires_in": 3600,
        "refresh_expires_in": 604800,
        "user": {
            "id": 123,
            "username": "joao_silva",
            "email": "joao.silva@email.com",
            "first_name": "João",
            "last_name": "Silva",
            "has_profile": True,
            "profile": {"cpf": "123.456.789-01", "ativo": True, "bairro": "Centro"},
        },
    },
    response_only=True,
)

JWT_TOKEN_OBTAIN_ERROR_EXAMPLE = OpenApiExample(
    "Credenciais Inválidas",
    summary="Login falhou",
    description="Resposta quando username ou senha estão incorretos",
    value={"detail": "No active account found with the given credentials"},
    response_only=True,
)

JWT_TOKEN_REFRESH_REQUEST_EXAMPLE = OpenApiExample(
    "Renovar Token",
    summary="Solicitação de renovação",
    description="Refresh token para obter novo access token",
    value={
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5NjYwMTM5OSwiaWF0IjoxNjk1OTk2Mzk5LCJqdGkiOiI5ODc2NTQzMjEwIiwidXNlcl9pZCI6MTIzfQ.signature"
    },
    request_only=True,
)

JWT_TOKEN_REFRESH_SUCCESS_EXAMPLE = OpenApiExample(
    "Token Renovado",
    summary="Novo access token gerado",
    description="Resposta com novo access token e refresh token rotacionado",
    value={
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk2MDAwNTk5LCJpYXQiOjE2OTU5OTY5OTksImp0aSI6IjExMTExMTExMTEiLCJ1c2VyX2lkIjoxMjN9.new_signature",
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5NjYwMTc5OSwiaWF0IjoxNjk1OTk2OTk5LCJqdGkiOiIyMjIyMjIyMjIyIiwidXNlcl9pZCI6MTIzfQ.new_refresh_signature",
        "token_type": "Bearer",
        "expires_in": 3600,
    },
    response_only=True,
)

JWT_TOKEN_VERIFY_REQUEST_EXAMPLE = OpenApiExample(
    "Verificar Token",
    summary="Token para verificação",
    description="Access ou refresh token para validar",
    value={
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk1OTk5OTk5LCJpYXQiOjE2OTU5OTYzOTksImp0aSI6IjEyMzQ1Njc4OTAiLCJ1c2VyX2lkIjoxMjN9.signature"
    },
    request_only=True,
)

JWT_TOKEN_INVALID_EXAMPLE = OpenApiExample(
    "Token Inválido",
    summary="Token expirado ou malformado",
    description="Resposta quando token não é válido",
    value={"detail": "Token is invalid or expired", "code": "token_not_valid"},
    response_only=True,
)

JWT_TOKEN_OBTAIN_DETAILED_SCHEMA = extend_schema(
    operation_id="jwt_token_obtain_detailed",
    summary="Obter tokens JWT (Login)",
    description="""
    Autentica o usuário e retorna tokens JWT com informações completas.

    **🔐 Processo de Autenticação:**
    1. Valida credenciais (username + password)
    2. Gera access token (60 minutos)
    3. Gera refresh token (7 dias)
    4. Inclui dados do usuário e perfil no token
    5. Retorna resposta completa

    **🎫 Access Token:**
    - **Validade**: 60 minutos
    - **Uso**: Autenticação em APIs
    - **Header**: `Authorization: Bearer <access_token>`
    - **Conteúdo**: Dados do usuário e perfil

    **🔄 Refresh Token:**
    - **Validade**: 7 dias
    - **Uso**: Renovar access token
    - **Rotação**: Novo refresh token a cada renovação
    - **Blacklist**: Tokens antigos são invalidados

    **👤 Dados Incluídos no Token:**
    - ID do usuário
    - Username e email
    - Nome completo
    - Status do perfil
    - CPF formatado (se perfil existe)
    - Status ativo do perfil

    **🔒 Segurança:**
    - Algoritmo HS256
    - Chave secreta do Django
    - Blacklist automática
    - Rotação de tokens
    - Expiração automática

    **💡 Como Usar:**
    ```bash
    POST /api/token/
    {"username": "usuario", "password": "senha"}

    GET /accounts/me/
    Authorization: Bearer <access_token>

    POST /api/token/refresh/
    {"refresh": "<refresh_token>"}
    ```
    """,
    tags=["JWT Authentication"],
    examples=[JWT_TOKEN_OBTAIN_REQUEST_EXAMPLE],
    responses={
        200: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Login realizado com sucesso",
            examples=[JWT_TOKEN_OBTAIN_SUCCESS_EXAMPLE],
        ),
        401: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Credenciais inválidas",
            examples=[JWT_TOKEN_OBTAIN_ERROR_EXAMPLE],
        ),
        400: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Dados de login inválidos",
            examples=[
                OpenApiExample(
                    "Campos Obrigatórios",
                    value={
                        "username": ["Este campo é obrigatório."],
                        "password": ["Este campo é obrigatório."],
                    },
                )
            ],
        ),
    },
)

JWT_TOKEN_REFRESH_DETAILED_SCHEMA = extend_schema(
    operation_id="jwt_token_refresh_detailed",
    summary="Renovar access token",
    description="""
    Renova o access token usando o refresh token.

    **🔄 Processo de Renovação:**
    1. Valida o refresh token
    2. Verifica se não está na blacklist
    3. Gera novo access token
    4. Rotaciona refresh token (novo refresh token)
    5. Adiciona token antigo à blacklist

    **⚙️ Configurações:**
    - **Rotação habilitada**: Novo refresh token a cada renovação
    - **Blacklist ativa**: Tokens antigos são invalidados
    - **Update last login**: Atualiza último acesso do usuário

    **🕐 Timing:**
    - **Access token**: 60 minutos de validade
    - **Refresh token**: 7 dias de validade
    - **Renovação**: Pode ser feita a qualquer momento
    - **Expiração**: Tokens expirados são rejeitados

    **🔒 Segurança:**
    - Refresh token é de uso único (rotação)
    - Tokens antigos são blacklistados
    - Validação rigorosa de assinatura
    - Proteção contra replay attacks

    **💡 Estratégias de Uso:**

    **Renovação Proativa:**
    ```javascript
    // Renovar antes de expirar (ex: 5 min antes)
    if (tokenExpiresIn < 300) {
        await refreshToken();
    }
    ```

    **Renovação Reativa:**
    ```javascript
    // Renovar quando receber 401
    if (response.status === 401) {
        await refreshToken();
        // Repetir requisição original
    }
    ```

    **⚠️ Importante:**
    - Guarde o novo refresh token
    - Descarte o refresh token antigo
    - Trate erros de token expirado
    - Implemente logout em caso de falha
    """,
    tags=["JWT Authentication"],
    examples=[JWT_TOKEN_REFRESH_REQUEST_EXAMPLE],
    responses={
        200: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Token renovado com sucesso",
            examples=[JWT_TOKEN_REFRESH_SUCCESS_EXAMPLE],
        ),
        401: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Refresh token inválido ou expirado",
            examples=[JWT_TOKEN_INVALID_EXAMPLE],
        ),
        400: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Refresh token não fornecido",
            examples=[
                OpenApiExample(
                    "Token Obrigatório",
                    value={"refresh": ["Este campo é obrigatório."]},
                )
            ],
        ),
    },
)

JWT_TOKEN_VERIFY_DETAILED_SCHEMA = extend_schema(
    operation_id="jwt_token_verify_detailed",
    summary="Verificar validade do token",
    description="""
    Verifica se um token JWT é válido e não expirou.

    **🔍 Validações Realizadas:**

    **📝 Estrutura:**
    - Formato JWT válido (header.payload.signature)
    - Algoritmo correto (HS256)
    - Assinatura válida

    **⏰ Tempo:**
    - Token não expirado
    - Timestamp válido
    - Fuso horário correto

    **🚫 Blacklist:**
    - Token não está na blacklist
    - JTI (JWT ID) único
    - Não foi revogado

    **👤 Usuário:**
    - Usuário existe no sistema
    - Conta está ativa
    - Permissões válidas

    **💡 Casos de Uso:**

    **Debug de Autenticação:**
    ```bash
    POST /api/token/verify/
    {"token": "seu_access_token"}
    ```

    **Validação Frontend:**
    ```javascript
    // Verificar antes de fazer requisições
    const isValid = await verifyToken(accessToken);
    if (!isValid) {
        await refreshToken();
    }
    ```

    **Health Check:**
    ```bash
    curl -X POST /api/token/verify/ \
      -H "Content-Type: application/json" \
      -d '{"token": "token_to_check"}'
    ```

    **🎯 Tipos de Token Aceitos:**
    - Access tokens
    - Refresh tokens
    - Qualquer token JWT válido do sistema

    **📊 Resposta:**
    - **Sucesso**: Status 200 (token válido)
    - **Erro**: Status 401 (token inválido)
    - **Detalhes**: Código de erro específico

    **⚠️ Notas:**
    - Não renova tokens automaticamente
    - Apenas verifica validade
    - Use para debug e validação
    - Não expõe dados sensíveis
    """,
    tags=["JWT Authentication"],
    examples=[JWT_TOKEN_VERIFY_REQUEST_EXAMPLE],
    responses={
        200: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Token válido",
            examples=[
                OpenApiExample(
                    "Token Válido",
                    summary="Token passou em todas as validações",
                    value={},
                )
            ],
        ),
        401: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Token inválido",
            examples=[
                JWT_TOKEN_INVALID_EXAMPLE,
                OpenApiExample(
                    "Token Expirado",
                    summary="Token expirou",
                    value={"detail": "Token is expired", "code": "token_expired"},
                ),
                OpenApiExample(
                    "Token Malformado",
                    summary="Token com formato inválido",
                    value={"detail": "Token is invalid", "code": "token_invalid"},
                ),
                OpenApiExample(
                    "Token Blacklistado",
                    summary="Token foi revogado",
                    value={
                        "detail": "Token is blacklisted",
                        "code": "token_blacklisted",
                    },
                ),
            ],
        ),
        400: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Token não fornecido",
            examples=[
                OpenApiExample(
                    "Token Obrigatório", value={"token": ["Este campo é obrigatório."]}
                )
            ],
        ),
    },
)

JWT_CONFIGURATION_INFO = {
    "algorithm": "HS256",
    "access_token_lifetime": "60 minutes",
    "refresh_token_lifetime": "7 days",
    "rotate_refresh_tokens": True,
    "blacklist_after_rotation": True,
    "update_last_login": True,
    "auth_header_types": ["Bearer"],
    "auth_header_name": "HTTP_AUTHORIZATION",
    "user_id_field": "id",
    "user_id_claim": "user_id",
    "token_type_claim": "token_type",
    "jti_claim": "jti",
}
