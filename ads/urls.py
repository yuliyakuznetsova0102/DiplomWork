from django.urls import path
from .views import (
    AdListCreateView,
    AdRetrieveUpdateDestroyView,
    CommentListCreateView,
    CommentRetrieveUpdateDestroyView,
)

urlpatterns = [
    path('ads/', AdListCreateView.as_view(), name='ad-list'),
    path('ads/<int:pk>/', AdRetrieveUpdateDestroyView.as_view(), name='ad-detail'),
    path('ads/<int:ad_id>/comments/', CommentListCreateView.as_view(), name='comment-list'),
    path('ads/<int:ad_id>/comments/<int:pk>/', CommentRetrieveUpdateDestroyView.as_view(), name='comment-detail'),
]