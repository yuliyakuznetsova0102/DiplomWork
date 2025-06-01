from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Ad, Comment
from .serializers import (
    AdSerializer,
    AdCreateSerializer,
    CommentSerializer,
    CommentCreateSerializer,
)
from .permissions import IsOwnerOrAdmin, IsCommentOwnerOrAdmin
from .filters import AdFilter


class AdListCreateView(generics.ListCreateAPIView):
    queryset = Ad.objects.all().order_by('-created_at')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = AdFilter
    search_fields = ['title']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AdCreateSerializer
        return AdSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AdRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrAdmin]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return AdCreateSerializer
        return AdSerializer


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        ad_id = self.kwargs['ad_id']
        return Comment.objects.filter(ad_id=ad_id).order_by('created_at')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentCreateSerializer
        return CommentSerializer

    def perform_create(self, serializer):
        ad_id = self.kwargs['ad_id']
        serializer.save(author=self.request.user, ad_id=ad_id)


class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsCommentOwnerOrAdmin]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return CommentCreateSerializer
        return CommentSerializer
