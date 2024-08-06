from rest_framework import serializers
from .models import Playlist


class PlaylistSerializer(serializers.ModelSerializer):
	medias_count = serializers.IntegerField(source='get_medias_count', read_only=True)

	class Meta:
		model = Playlist
		fields = ['id', 'title', 'user', 'timestamp', 'slug', 'medias_count']
