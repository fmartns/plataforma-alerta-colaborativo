"""
Serializers modulares para o app alerts
"""

from .alert import AlertSerializer, AlertCreateSerializer, AlertUpdateSerializer, AlertListSerializer, AlertStatsSerializer
from .post import PostSerializer, PostCreateSerializer, PostUpdateSerializer, PostListSerializer, PostStatsSerializer
from .comment import CommentSerializer, CommentCreateSerializer, CommentUpdateSerializer, CommentListSerializer, CommentStatsSerializer

__all__ = [
    'AlertSerializer',
    'AlertCreateSerializer', 
    'AlertUpdateSerializer',
    'AlertListSerializer',
    'AlertStatsSerializer',
    'PostSerializer',
    'PostCreateSerializer',
    'PostUpdateSerializer', 
    'PostListSerializer',
    'PostStatsSerializer',
    'CommentSerializer',
    'CommentCreateSerializer',
    'CommentUpdateSerializer',
    'CommentListSerializer',
    'CommentStatsSerializer',
]
