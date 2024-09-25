from rest_framework import serializers

from .models import Media, MediaLike, MediaView


class MediaSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(source='get_likes_count', read_only=True)
    views_count = serializers.IntegerField(source='get_views_count', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    avatar_url = serializers.ImageField(source='user.profile.avatar', read_only=True)

    class Meta:
        model = Media
        fields = [
            'id', 'user', 'username', 'avatar_url', 'is_private', 'title',
            'description', 'text', 'media', 'original', 'slug', 'timestamp',
            'downloads_count', 'tags', 'likes_count', 'views_count'
        ]


    def to_representation(self, instance):
        """
        Custom representation to hide private media if the current user
        does not have access.
        """

        if instance.is_private:
            return {}

        return super().to_representation(instance)


class MediaLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaLike
        fields = ['id', 'user', 'media', 'timestamp']


class MediaViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaView
        fields = ['id', 'user', 'media', 'timestamp']