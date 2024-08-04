from django.contrib import admin

from .models import Media, MediaLike, MediaView


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'timestamp', 'is_private', 'tag_count')
    search_fields = ('title', 'description', 'user__username')
    list_filter = ('is_private', 'timestamp')

    def tag_count(self, obj):
        return obj.tags.count()

    tag_count.short_description = 'Tag Count'


@admin.register(MediaLike)
class MediaLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'media', 'timestamp')
    search_fields = ('user__username',)
    list_filter = ('timestamp',)


@admin.register(MediaView)
class MediaViewAdmin(admin.ModelAdmin):
    list_display = ('user', 'media', 'timestamp')
    search_fields = ('user__username',)
    list_filter = ('timestamp',)