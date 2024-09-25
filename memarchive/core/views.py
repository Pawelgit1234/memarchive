from django.shortcuts import render, get_object_or_404

from medias.models import Media
from medias.business import add_view
from users.models import Profile
from users.business import is_following


def home(request):
	return render(request, "core/home.html")


def media(request, slug):
	media = get_object_or_404(Media, slug=slug)

	user_liked = False
	user_following = False

	if request.user.is_authenticated:
		user_liked = media.likes.filter(user=request.user).exists()
		user_following = is_following(media.user.profile, request.user.profile)

	context = {
		'media': media,
		'user_liked': user_liked,
		'user_following': user_following,
	}

	add_view(media.id, request.user.id)

	return render(request, 'core/media.html', context)