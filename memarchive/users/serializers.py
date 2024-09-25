from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
	followers_count = serializers.IntegerField(source='get_followers_count', read_only=True)
	username = serializers.CharField(source='user.username', read_only=True)
	class Meta:
		model = Profile
		fields = ['user', 'avatar', 'bio', 'followers_count', 'username']