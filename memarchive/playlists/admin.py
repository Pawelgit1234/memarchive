from django.contrib import admin

from .models import Playlist


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
	list_display = ('user', 'title', 'timestamp', 'media_count')
	search_fields = ('user__username', 'title')
	list_filter = ('timestamp',)
