"""
URLs para o app alerts
"""

from django.urls import path
from .views import (
    AlertCreateAPIView,
    AlertListAPIView,
    AlertDetailAPIView,
    AlertStatsAPIView,
    PostCreateAPIView,
    PostListAPIView,
    PostDetailAPIView,
    PostFeedAPIView,
    PostStatsAPIView,
    CommentCreateAPIView,
    CommentListAPIView,
    CommentDetailAPIView,
    CommentStatsAPIView,
    AdminAlertListAPIView,
    AdminPostListAPIView,
    AdminCommentListAPIView,
)

app_name = 'alerts'

urlpatterns = [
    path('alerts/', AlertCreateAPIView.as_view(), name='alert-create'),
    path('alerts/list/', AlertListAPIView.as_view(), name='alert-list'),
    path('alerts/<int:alert_id>/', AlertDetailAPIView.as_view(), name='alert-detail'),
    path('alerts/stats/', AlertStatsAPIView.as_view(), name='alert-stats'),
    
    path('posts/', PostCreateAPIView.as_view(), name='post-create'),
    path('posts/list/', PostListAPIView.as_view(), name='post-list'),
    path('posts/<int:post_id>/', PostDetailAPIView.as_view(), name='post-detail'),
    path('posts/stats/', PostStatsAPIView.as_view(), name='post-stats'),
    
    path('feed/', PostFeedAPIView.as_view(), name='post-feed'),
    path('feed/<int:post_id>/', PostFeedAPIView.as_view(), name='post-view'),
    
    path('comments/', CommentCreateAPIView.as_view(), name='comment-create'),
    path('comments/post/<int:post_id>/', CommentListAPIView.as_view(), name='comment-list'),
    path('comments/<int:comment_id>/', CommentDetailAPIView.as_view(), name='comment-detail'),
    path('comments/stats/', CommentStatsAPIView.as_view(), name='comment-stats'),
    
    path('admin/alerts/', AdminAlertListAPIView.as_view(), name='admin-alert-list'),
    path('admin/alerts/<int:alert_id>/', AdminAlertListAPIView.as_view(), name='admin-alert-update'),
    path('admin/posts/', AdminPostListAPIView.as_view(), name='admin-post-list'),
    path('admin/comments/', AdminCommentListAPIView.as_view(), name='admin-comment-list'),
    path('admin/comments/<int:comment_id>/', AdminCommentListAPIView.as_view(), name='admin-comment-moderate'),
]

