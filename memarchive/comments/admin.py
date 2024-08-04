from django.contrib import admin

from .models import Comment, CommentLike


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'short_content', 'media', 'timestamp', 'parent')
    search_fields = ('content', 'user__username')
    list_filter = ('timestamp',)

    def short_content(self, obj):
        max_length = 50
        if len(obj.content) > max_length:
            return f'{obj.content[:max_length]}...'
        return obj.content

    short_content.short_description = 'Content'


@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'timestamp')
    search_fields = ('user__username',)
    list_filter = ('timestamp',)