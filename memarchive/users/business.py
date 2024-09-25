from .models import Profile


def follow(profile: Profile, follower: Profile):
	profile.following.add(follower)


def unfollow(profile: Profile, follower: Profile):
	profile.following.remove(follower)


def is_following(profile: Profile, follower: Profile) -> bool:
	return profile.following.filter(pk=follower.pk).exists()