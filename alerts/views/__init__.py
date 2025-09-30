"""
Views modulares para o app alerts
"""

from .alert import AlertCreateAPIView, AlertListAPIView, AlertDetailAPIView, AlertStatsAPIView
from .post import PostCreateAPIView, PostListAPIView, PostDetailAPIView, PostFeedAPIView, PostStatsAPIView
from .comment import CommentCreateAPIView, CommentListAPIView, CommentDetailAPIView, CommentStatsAPIView
from .admin import AdminAlertListAPIView, AdminPostListAPIView, AdminCommentListAPIView

__all__ = [
    'AlertCreateAPIView',
    'AlertListAPIView', 
    'AlertDetailAPIView',
    'AlertStatsAPIView',
    'PostCreateAPIView',
    'PostListAPIView',
    'PostDetailAPIView',
    'PostFeedAPIView',
    'PostStatsAPIView',
    'CommentCreateAPIView',
    'CommentListAPIView',
    'CommentDetailAPIView',
    'CommentStatsAPIView',
    'AdminAlertListAPIView',
    'AdminPostListAPIView',
    'AdminCommentListAPIView',
]
