from rest_framework import serializers
from .models import Media, MediaLike, MediaView


class MediaSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(source='get_likes_count', read_only=True)
    views_count = serializers.IntegerField(source='get_views_count', read_only=True)

    class Meta:
        model = Media
        fields = [
            'id', 'user', 'is_private', 'title', 'description', 'text', 'media',
            'original', 'slug', 'timestamp', 'downloads_count', 'tags',
            'likes_count', 'views_count'
        ]


class MediaLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaLike
        fields = ['id', 'user', 'media', 'timestamp']


class MediaViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaView
        fields = ['id', 'user', 'media', 'timestamp']