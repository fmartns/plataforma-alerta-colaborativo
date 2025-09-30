"""
Schemas simplificados para documentação das APIs do app alerts
"""

from drf_spectacular.utils import extend_schema
from drf_spectacular.openapi import OpenApiResponse
from rest_framework import status

ALERT_CREATE_SIMPLE_SCHEMA = extend_schema(
    operation_id="alert_create",
    summary="Criar Alerta",
    description="Criar novo alerta de desastre",
    tags=["Alertas"],
    responses={
        201: OpenApiResponse(description="Alerta criado com sucesso"),
        400: OpenApiResponse(description="Dados inválidos"),
        401: OpenApiResponse(description="Não autenticado"),
    }
)

ALERT_LIST_SIMPLE_SCHEMA = extend_schema(
    operation_id="alert_list",
    summary="Listar Alertas",
    description="Listar alertas do usuário",
    tags=["Alertas"],
    responses={
        200: OpenApiResponse(description="Lista de alertas"),
        401: OpenApiResponse(description="Não autenticado"),
    }
)

ALERT_DETAIL_SIMPLE_SCHEMA = extend_schema(
    operation_id="alert_detail",
    summary="Detalhes do Alerta",
    description="Obter detalhes de um alerta específico",
    tags=["Alertas"],
    responses={
        200: OpenApiResponse(description="Detalhes do alerta"),
        404: OpenApiResponse(description="Alerta não encontrado"),
        401: OpenApiResponse(description="Não autenticado"),
    }
)

ALERT_UPDATE_SIMPLE_SCHEMA = extend_schema(
    operation_id="alert_update",
    summary="Atualizar Alerta",
    description="Atualizar alerta existente",
    tags=["Alertas"],
    responses={
        200: OpenApiResponse(description="Alerta atualizado"),
        400: OpenApiResponse(description="Dados inválidos"),
        404: OpenApiResponse(description="Alerta não encontrado"),
        401: OpenApiResponse(description="Não autenticado"),
    }
)

ALERT_DELETE_SIMPLE_SCHEMA = extend_schema(
    operation_id="alert_delete",
    summary="Excluir Alerta",
    description="Excluir alerta (soft delete)",
    tags=["Alertas"],
    responses={
        200: OpenApiResponse(description="Alerta excluído"),
        400: OpenApiResponse(description="Não é possível excluir"),
        404: OpenApiResponse(description="Alerta não encontrado"),
        401: OpenApiResponse(description="Não autenticado"),
    }
)

ALERT_STATS_SIMPLE_SCHEMA = extend_schema(
    operation_id="alert_stats",
    summary="Estatísticas de Alertas",
    description="Obter estatísticas dos alertas do usuário",
    tags=["Alertas"],
    responses={
        200: OpenApiResponse(description="Estatísticas dos alertas"),
        401: OpenApiResponse(description="Não autenticado"),
    }
)

POST_CREATE_SIMPLE_SCHEMA = extend_schema(
    operation_id="post_create",
    summary="Criar Post",
    description="Criar novo post da Defesa Civil",
    tags=["Posts"],
    responses={
        201: OpenApiResponse(description="Post criado com sucesso"),
        400: OpenApiResponse(description="Dados inválidos"),
        401: OpenApiResponse(description="Não autenticado"),
        403: OpenApiResponse(description="Sem permissão de administrador"),
    }
)

POST_LIST_SIMPLE_SCHEMA = extend_schema(
    operation_id="post_list",
    summary="Listar Posts",
    description="Listar posts para administradores",
    tags=["Posts"],
    responses={
        200: OpenApiResponse(description="Lista de posts"),
        401: OpenApiResponse(description="Não autenticado"),
        403: OpenApiResponse(description="Sem permissão de administrador"),
    }
)

POST_DETAIL_SIMPLE_SCHEMA = extend_schema(
    operation_id="post_detail",
    summary="Detalhes do Post",
    description="Obter detalhes de um post específico",
    tags=["Posts"],
    responses={
        200: OpenApiResponse(description="Detalhes do post"),
        404: OpenApiResponse(description="Post não encontrado"),
        401: OpenApiResponse(description="Não autenticado"),
        403: OpenApiResponse(description="Sem permissão de administrador"),
    }
)

POST_UPDATE_SIMPLE_SCHEMA = extend_schema(
    operation_id="post_update",
    summary="Atualizar Post",
    description="Atualizar post existente",
    tags=["Posts"],
    responses={
        200: OpenApiResponse(description="Post atualizado"),
        400: OpenApiResponse(description="Dados inválidos"),
        404: OpenApiResponse(description="Post não encontrado"),
        401: OpenApiResponse(description="Não autenticado"),
        403: OpenApiResponse(description="Sem permissão de administrador"),
    }
)

POST_DELETE_SIMPLE_SCHEMA = extend_schema(
    operation_id="post_delete",
    summary="Arquivar Post",
    description="Arquivar post existente",
    tags=["Posts"],
    responses={
        200: OpenApiResponse(description="Post arquivado"),
        404: OpenApiResponse(description="Post não encontrado"),
        401: OpenApiResponse(description="Não autenticado"),
        403: OpenApiResponse(description="Sem permissão de administrador"),
    }
)

POST_FEED_SIMPLE_SCHEMA = extend_schema(
    operation_id="post_feed",
    summary="Feed de Posts",
    description="Feed público de posts publicados",
    tags=["Feed Público"],
    responses={
        200: OpenApiResponse(description="Feed de posts"),
    }
)

POST_VIEW_SIMPLE_SCHEMA = extend_schema(
    operation_id="post_view",
    summary="Visualizar Post",
    description="Visualizar post específico e incrementar contador",
    tags=["Feed Público"],
    responses={
        200: OpenApiResponse(description="Detalhes do post"),
        404: OpenApiResponse(description="Post não encontrado"),
    }
)

POST_STATS_SIMPLE_SCHEMA = extend_schema(
    operation_id="post_stats",
    summary="Estatísticas de Posts",
    description="Obter estatísticas dos posts",
    tags=["Posts"],
    responses={
        200: OpenApiResponse(description="Estatísticas dos posts"),
        401: OpenApiResponse(description="Não autenticado"),
        403: OpenApiResponse(description="Sem permissão de administrador"),
    }
)

COMMENT_CREATE_SIMPLE_SCHEMA = extend_schema(
    operation_id="comment_create",
    summary="Criar Comentário",
    description="Criar novo comentário em um post",
    tags=["Comentários"],
    responses={
        201: OpenApiResponse(description="Comentário criado com sucesso"),
        400: OpenApiResponse(description="Dados inválidos"),
        401: OpenApiResponse(description="Não autenticado"),
    }
)

COMMENT_LIST_SIMPLE_SCHEMA = extend_schema(
    operation_id="comment_list",
    summary="Listar Comentários",
    description="Listar comentários de um post",
    tags=["Comentários"],
    responses={
        200: OpenApiResponse(description="Lista de comentários"),
        404: OpenApiResponse(description="Post não encontrado"),
    }
)

COMMENT_DETAIL_SIMPLE_SCHEMA = extend_schema(
    operation_id="comment_detail",
    summary="Detalhes do Comentário",
    description="Obter detalhes de um comentário específico",
    tags=["Comentários"],
    responses={
        200: OpenApiResponse(description="Detalhes do comentário"),
        404: OpenApiResponse(description="Comentário não encontrado"),
        401: OpenApiResponse(description="Não autenticado"),
    }
)

COMMENT_UPDATE_SIMPLE_SCHEMA = extend_schema(
    operation_id="comment_update",
    summary="Atualizar Comentário",
    description="Atualizar comentário existente",
    tags=["Comentários"],
    responses={
        200: OpenApiResponse(description="Comentário atualizado"),
        400: OpenApiResponse(description="Dados inválidos ou tempo limite excedido"),
        404: OpenApiResponse(description="Comentário não encontrado"),
        401: OpenApiResponse(description="Não autenticado"),
    }
)

COMMENT_DELETE_SIMPLE_SCHEMA = extend_schema(
    operation_id="comment_delete",
    summary="Excluir Comentário",
    description="Excluir comentário (soft delete)",
    tags=["Comentários"],
    responses={
        200: OpenApiResponse(description="Comentário excluído"),
        400: OpenApiResponse(description="Tempo limite excedido"),
        404: OpenApiResponse(description="Comentário não encontrado"),
        401: OpenApiResponse(description="Não autenticado"),
    }
)

COMMENT_STATS_SIMPLE_SCHEMA = extend_schema(
    operation_id="comment_stats",
    summary="Estatísticas de Comentários",
    description="Obter estatísticas dos comentários",
    tags=["Comentários"],
    responses={
        200: OpenApiResponse(description="Estatísticas dos comentários"),
        401: OpenApiResponse(description="Não autenticado"),
        403: OpenApiResponse(description="Sem permissão de administrador"),
    }
)

ADMIN_ALERT_LIST_SIMPLE_SCHEMA = extend_schema(
    operation_id="admin_alert_list",
    summary="Listar Alertas (Admin)",
    description="Listar todos os alertas para administradores",
    tags=["Administração"],
    responses={
        200: OpenApiResponse(description="Lista de alertas"),
        401: OpenApiResponse(description="Não autenticado"),
        403: OpenApiResponse(description="Sem permissão de administrador"),
    }
)

ADMIN_ALERT_UPDATE_SIMPLE_SCHEMA = extend_schema(
    operation_id="admin_alert_update",
    summary="Atualizar Alerta (Admin)",
    description="Atualizar status de alerta",
    tags=["Administração"],
    responses={
        200: OpenApiResponse(description="Alerta atualizado"),
        400: OpenApiResponse(description="Dados inválidos"),
        404: OpenApiResponse(description="Alerta não encontrado"),
        401: OpenApiResponse(description="Não autenticado"),
        403: OpenApiResponse(description="Sem permissão de administrador"),
    }
)

ADMIN_POST_LIST_SIMPLE_SCHEMA = extend_schema(
    operation_id="admin_post_list",
    summary="Listar Posts (Admin)",
    description="Listar posts com filtros administrativos",
    tags=["Administração"],
    responses={
        200: OpenApiResponse(description="Lista de posts"),
        401: OpenApiResponse(description="Não autenticado"),
        403: OpenApiResponse(description="Sem permissão de administrador"),
    }
)

ADMIN_COMMENT_LIST_SIMPLE_SCHEMA = extend_schema(
    operation_id="admin_comment_list",
    summary="Listar Comentários (Admin)",
    description="Listar comentários com filtros administrativos",
    tags=["Administração"],
    responses={
        200: OpenApiResponse(description="Lista de comentários"),
        401: OpenApiResponse(description="Não autenticado"),
        403: OpenApiResponse(description="Sem permissão de administrador"),
    }
)

ADMIN_COMMENT_MODERATE_SIMPLE_SCHEMA = extend_schema(
    operation_id="admin_comment_moderate",
    summary="Moderar Comentário",
    description="Aprovar, rejeitar ou excluir comentário",
    tags=["Administração"],
    responses={
        200: OpenApiResponse(description="Comentário moderado"),
        400: OpenApiResponse(description="Ação inválida"),
        404: OpenApiResponse(description="Comentário não encontrado"),
        401: OpenApiResponse(description="Não autenticado"),
        403: OpenApiResponse(description="Sem permissão de administrador"),
    }
)

