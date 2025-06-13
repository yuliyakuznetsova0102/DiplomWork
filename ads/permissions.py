from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    "Разрешение, позволяющее доступ только владельцу объявления или администратору."
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.user.is_admin:
                return True
            return obj.author == request.user
        return False


class IsCommentOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.user.is_admin:
                return True
            return obj.author == request.user
        return False
