from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_joined', 'avatar_image')
    search_fields = ('user__username',)
    list_filter = ('user__date_joined',)

    def date_joined(self, obj):
        return obj.user.date_joined

    date_joined.admin_order_field = 'user__date_joined'
    date_joined.short_description = 'Date Joined'

    def avatar_image(self, obj):
        if obj.avatar:
            return mark_safe(f'<img src="{obj.avatar.url}" width="20" height="20" />')
        return 'No image'

    avatar_image.short_description = 'Avatar'
