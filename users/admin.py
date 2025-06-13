from django.contrib import admin
from ads.models import Ad, Comment
from django.contrib.auth.models import Group


admin.site.unregister(Group)


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'author', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('title', 'author__email')
    readonly_fields = ('title', 'price', 'description', 'author', 'created_at')

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('short_text', 'author', 'ad', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('text', 'author__email')

    def short_text(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text

    short_text.short_description = 'Text'

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
