"""
Documentação Swagger/OpenAPI para rotas de validação
"""

from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiResponse,
    OpenApiParameter,
)
from drf_spectacular.openapi import OpenApiTypes

CPF_VALID_RESPONSE_EXAMPLE = OpenApiExample(
    "CPF Válido e Disponível",
    summary="CPF válido e disponível para cadastro",
    description="Resposta quando CPF é válido e não está em uso",
    value={
        "cpf": "12345678901",
        "cpf_formatted": "123.456.789-01",
        "available": True,
        "message": "CPF disponível para cadastro",
    },
    response_only=True,
)

CPF_UNAVAILABLE_RESPONSE_EXAMPLE = OpenApiExample(
    "CPF Já Cadastrado",
    summary="CPF válido mas já em uso",
    description="Resposta quando CPF é válido mas já está cadastrado",
    value={
        "cpf": "98765432100",
        "cpf_formatted": "987.654.321-00",
        "available": False,
        "message": "CPF já cadastrado no sistema",
    },
    response_only=True,
)

CPF_INVALID_RESPONSE_EXAMPLE = OpenApiExample(
    "CPF Inválido",
    summary="CPF com formato ou algoritmo inválido",
    description="Resposta quando CPF não passa na validação",
    value={"error": "CPF inválido."},
    response_only=True,
)

PHONE_VALID_RESPONSE_EXAMPLE = OpenApiExample(
    "Telefone Válido",
    summary="Telefone brasileiro válido",
    description="Resposta para telefone com formato correto",
    value={
        "phone": "48999887766",
        "phone_formatted": "(48) 99988-7766",
        "valid": True,
        "message": "Telefone válido",
    },
    response_only=True,
)

PHONE_INVALID_RESPONSE_EXAMPLE = OpenApiExample(
    "Telefone Inválido",
    summary="Telefone com formato incorreto",
    description="Resposta para telefone inválido",
    value={
        "phone": "123456",
        "valid": False,
        "error": "Telefone deve ter 10 ou 11 dígitos (com DDD).",
    },
    response_only=True,
)

CEP_VALID_RESPONSE_EXAMPLE = OpenApiExample(
    "CEP Válido",
    summary="CEP brasileiro válido",
    description="Resposta para CEP com formato correto",
    value={
        "cep": "88010000",
        "cep_formatted": "88010-000",
        "valid": True,
        "message": "CEP válido",
    },
    response_only=True,
)

CEP_INVALID_RESPONSE_EXAMPLE = OpenApiExample(
    "CEP Inválido",
    summary="CEP com formato incorreto",
    description="Resposta para CEP inválido",
    value={"cep": "123", "valid": False, "error": "CEP deve ter 8 dígitos."},
    response_only=True,
)

NEIGHBORHOODS_RESPONSE_EXAMPLE = OpenApiExample(
    "Lista de Bairros",
    summary="Bairros de Florianópolis",
    description="Lista completa dos bairros aceitos pelo sistema",
    value={
        "neighborhoods": [
            "Abraão",
            "Agronômica",
            "Alto Ribeirão",
            "Armação",
            "Balneário",
            "Barra da Lagoa",
            "Barra do Sambaqui",
            "Bom Abrigo",
            "Bom Retiro",
            "Cachoeira do Bom Jesus",
            "Cacupé",
            "Caieira da Barra do Sul",
            "Campeche",
            "Canasvieiras",
            "Canto",
            "Capoeiras",
            "Carvoeira",
            "Centro",
            "Coloninha",
            "Coqueiros",
            "Córrego Grande",
            "Costa de Dentro",
            "Costeira do Pirajubaé",
            "Daniela",
            "Estreito",
            "Galheta",
            "Ingleses",
            "Itacorubi",
            "Jardim Atlântico",
            "João Paulo",
            "Joaquina",
            "José Mendes",
            "Jurerê",
            "Jurerê Internacional",
            "Lagoinha",
            "Lagoinha do Leste",
            "Matadeiro",
            "Mole",
            "Monte Cristo",
            "Monte Verde",
            "Pantanal",
            "Pântano do Sul",
            "Ponta das Canas",
            "Praia Brava",
            "Prainha",
            "Ratones",
            "Ribeirão da Ilha",
            "Saco dos Limões",
            "Saco Grande",
            "Sambaqui",
            "Santa Mônica",
            "Santinho",
            "Santo Antônio de Lisboa",
            "Sede Fragas",
            "Serrinha",
            "Tapera",
            "Trindade",
            "Vargem do Bom Jesus",
            "Vargem Grande",
            "Vargem Pequena",
        ],
        "total": 57,
        "note": "Lista oficial de bairros de Florianópolis aceitos pelo sistema",
    },
    response_only=True,
)

CPF_VALIDATION_SCHEMA = extend_schema(
    operation_id="validate_cpf_availability",
    summary="Validar disponibilidade de CPF",
    description="""
    Verifica se um CPF é válido e está disponível para cadastro.

    **Validações Realizadas:**

    **🔍 Formato:**
    - Aceita CPF com ou sem formatação
    - Remove automaticamente pontos e hífens
    - Verifica se tem exatamente 11 dígitos

    **🧮 Algoritmo:**
    - Validação completa do algoritmo brasileiro
    - Cálculo dos dígitos verificadores
    - Rejeita CPFs com todos os dígitos iguais

    **💾 Disponibilidade:**
    - Verifica se CPF já está cadastrado
    - Busca em toda a base de dados
    - Retorna status de disponibilidade

    **📤 Resposta:**
    - CPF limpo (apenas números)
    - CPF formatado (XXX.XXX.XXX-XX)
    - Status de disponibilidade
    - Mensagem descritiva

    **💡 Casos de Uso:**
    - Validação em tempo real em formulários
    - Verificação antes do cadastro
    - Integração com frontend
    """,
    tags=["Validação"],
    parameters=[
        OpenApiParameter(
            name="cpf",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="CPF a ser validado (com ou sem formatação)",
            required=True,
            examples=[
                OpenApiExample(
                    "CPF sem formatação",
                    summary="CPF apenas números",
                    value="12345678901",
                ),
                OpenApiExample(
                    "CPF formatado",
                    summary="CPF com pontos e hífen",
                    value="123.456.789-01",
                ),
                OpenApiExample(
                    "CPF com espaços",
                    summary="CPF com espaços extras",
                    value=" 123 456 789 01 ",
                ),
            ],
        )
    ],
    responses={
        200: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Validação realizada com sucesso",
            examples=[CPF_VALID_RESPONSE_EXAMPLE, CPF_UNAVAILABLE_RESPONSE_EXAMPLE],
        ),
        400: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="CPF inválido ou não fornecido",
            examples=[
                CPF_INVALID_RESPONSE_EXAMPLE,
                OpenApiExample(
                    "CPF Não Fornecido", value={"error": "CPF é obrigatório"}
                ),
                OpenApiExample(
                    "CPF Muito Curto", value={"error": "CPF deve ter 11 dígitos"}
                ),
            ],
        ),
    },
)

PHONE_VALIDATION_SCHEMA = extend_schema(
    operation_id="validate_phone_number",
    summary="Validar telefone brasileiro",
    description="""
    Valida formato de telefone brasileiro com DDD.

    **Formatos Aceitos:**

    **📱 Celular (11 dígitos):**
    - Formato: (XX) 9XXXX-XXXX
    - Terceiro dígito deve ser 9
    - Exemplo: 48999887766

    **☎️ Fixo (10 dígitos):**
    - Formato: (XX) XXXX-XXXX
    - Sem o dígito 9 inicial
    - Exemplo: 4833334444

    **🌍 DDD Válidos:**
    - Faixa: 11 a 99
    - Validação de DDDs brasileiros
    - Rejeita DDDs inválidos

    **🔧 Processamento:**
    - Remove caracteres não numéricos
    - Valida quantidade de dígitos
    - Verifica regras específicas
    - Formata para exibição

    **📤 Resposta:**
    - Telefone original
    - Telefone formatado
    - Status de validade
    - Mensagem de erro (se inválido)
    """,
    tags=["Validação"],
    parameters=[
        OpenApiParameter(
            name="phone",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Telefone a ser validado",
            required=True,
            examples=[
                OpenApiExample(
                    "Celular", summary="Celular com DDD", value="48999887766"
                ),
                OpenApiExample("Fixo", summary="Telefone fixo", value="4833334444"),
                OpenApiExample(
                    "Com formatação",
                    summary="Telefone formatado",
                    value="(48) 99988-7766",
                ),
                OpenApiExample(
                    "Com espaços",
                    summary="Telefone com espaços",
                    value="48 9 9988 7766",
                ),
            ],
        )
    ],
    responses={
        200: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Telefone válido",
            examples=[PHONE_VALID_RESPONSE_EXAMPLE],
        ),
        400: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Telefone inválido",
            examples=[
                PHONE_INVALID_RESPONSE_EXAMPLE,
                OpenApiExample(
                    "Telefone Não Fornecido", value={"error": "Telefone é obrigatório"}
                ),
                OpenApiExample(
                    "DDD Inválido",
                    value={
                        "phone": "0999887766",
                        "valid": False,
                        "error": "DDD inválido.",
                    },
                ),
            ],
        ),
    },
)

CEP_VALIDATION_SCHEMA = extend_schema(
    operation_id="validate_cep_format",
    summary="Validar CEP brasileiro",
    description="""
    Valida formato de CEP brasileiro.

    **Formato Esperado:**
    - 8 dígitos numéricos
    - Com ou sem hífen
    - Exemplos: 88010000, 88010-000

    **Validações:**

    **📏 Comprimento:**
    - Exatamente 8 dígitos após limpeza
    - Remove hífens automaticamente
    - Rejeita CEPs muito curtos/longos

    **🚫 Valores Inválidos:**
    - CEP 00000000 (genérico)
    - Apenas letras ou símbolos
    - Formatos incorretos

    **🔧 Processamento:**
    - Remove caracteres não numéricos
    - Valida comprimento
    - Verifica valores especiais
    - Formata para exibição (XXXXX-XXX)

    **📤 Resposta:**
    - CEP original
    - CEP formatado
    - Status de validade
    - Mensagem de erro (se inválido)

    **⚠️ Limitações:**
    - Não verifica existência real
    - Apenas validação de formato
    - Para validação completa, use APIs dos Correios
    """,
    tags=["Validação"],
    parameters=[
        OpenApiParameter(
            name="cep",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="CEP a ser validado",
            required=True,
            examples=[
                OpenApiExample(
                    "CEP sem hífen", summary="CEP apenas números", value="88010000"
                ),
                OpenApiExample(
                    "CEP com hífen", summary="CEP formatado", value="88010-000"
                ),
                OpenApiExample(
                    "CEP com espaços", summary="CEP com espaços", value=" 88010 000 "
                ),
            ],
        )
    ],
    responses={
        200: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="CEP válido",
            examples=[CEP_VALID_RESPONSE_EXAMPLE],
        ),
        400: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="CEP inválido",
            examples=[
                CEP_INVALID_RESPONSE_EXAMPLE,
                OpenApiExample(
                    "CEP Não Fornecido", value={"error": "CEP é obrigatório"}
                ),
                OpenApiExample(
                    "CEP Genérico",
                    value={"cep": "00000000", "valid": False, "error": "CEP inválido."},
                ),
            ],
        ),
    },
)

NEIGHBORHOODS_LIST_SCHEMA = extend_schema(
    operation_id="list_florianopolis_neighborhoods",
    summary="Listar bairros de Florianópolis",
    description="""
    Retorna lista completa de bairros válidos de Florianópolis.

    **Finalidade:**
    - Validação de endereços
    - Preenchimento de formulários
    - Filtros de busca
    - Integração com frontend

    **Características:**

    **📍 Cobertura Completa:**
    - Todos os bairros oficiais de Florianópolis
    - Lista atualizada e verificada
    - Inclui bairros centrais e periféricos
    - Cobertura de toda a ilha

    **🔤 Ordenação:**
    - Ordem alfabética
    - Facilita busca visual
    - Consistente entre chamadas

    **📊 Metadados:**
    - Total de bairros
    - Nota explicativa
    - Informações adicionais

    **💡 Casos de Uso:**
    - Dropdown/select em formulários
    - Autocomplete de endereços
    - Validação de bairros
    - Filtros de busca geográfica

    **🔄 Atualização:**
    - Lista estática otimizada
    - Cache-friendly
    - Resposta rápida
    - Sem consulta ao banco

    **🎯 Integração:**
    - Usar com validação de perfis
    - Combinar com APIs de CEP
    - Filtros administrativos
    """,
    tags=["Validação"],
    responses={
        200: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="Lista de bairros obtida com sucesso",
            examples=[NEIGHBORHOODS_RESPONSE_EXAMPLE],
        )
    },
)
