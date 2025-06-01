from rest_framework import serializers
from .models import Ad, Comment
from users.serializers import UserSerializer


class AdSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Ad
        fields = ['id', 'title', 'price', 'description', 'author', 'created_at']


class AdCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ['title', 'price', 'description']


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'ad', 'created_at']
        read_only_fields = ['ad']


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['text']