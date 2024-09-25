from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView

from .models import Profile
from .serializers import ProfileSerializer
from .business import *


class ProfileListView(ListAPIView):
	""" List all profiles with pagination, or create a new profile """
	queryset = Profile.objects.all()
	serializer_class = ProfileSerializer

	def post(self, request, *args, **kwargs):
		serializer = ProfileSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileDetailView(RetrieveUpdateDestroyAPIView):
	""" Retrieve, update or delete a profile """
	queryset = Profile.objects.all()
	serializer_class = ProfileSerializer


class FollowProfileView(GenericAPIView):
	""" Follow or unfollow a profile """
	permission_classes = [IsAuthenticated]

	def post(self, request, pk):
		try:
			profile_to_follow = Profile.objects.get(pk=pk)
		except Profile.DoesNotExist:
			return Response({'error': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)

		user_profile = request.user.profile

		if is_following(profile_to_follow, user_profile):
			return Response({'error': 'You are already following this user.'}, status=status.HTTP_400_BAD_REQUEST)

		follow(profile_to_follow, user_profile)
		return Response({'is_following': True, 'followers_count': profile_to_follow.get_followers_count()}, status=status.HTTP_200_OK)

	def delete(self, request, pk):
		try:
			profile_to_unfollow = Profile.objects.get(pk=pk)
		except Profile.DoesNotExist:
			return Response({'error': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)

		user_profile = request.user.profile

		if not is_following(profile_to_unfollow, user_profile):
			return Response({'error': 'You are not following this user.'}, status=status.HTTP_400_BAD_REQUEST)

		unfollow(profile_to_unfollow, user_profile)
		return Response({'is_following': False, 'followers_count': profile_to_unfollow.get_followers_count()}, status=status.HTTP_200_OK)