from rest_framework import serializers
from .models import Comment, CommentLike


class CommentSerializer(serializers.ModelSerializer):
	likes_count = serializers.IntegerField(source='get_likes_count', read_only=True)

	class Meta:
		model = Comment
		fields = ['id', 'content', 'user', 'media', 'parent', 'timestamp', 'is_modified', 'likes_count']


class CommentLikeSerializer(serializers.ModelSerializer):
	class Meta:
		model = CommentLike
		fields = ['id', 'user', 'comment', 'timestamp']