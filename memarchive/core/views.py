from django.shortcuts import render, get_object_or_404

from medias.models import Media


def home(request):
	return render(request, "core/home.html")


def media(request, slug):
	media = get_object_or_404(Media, slug=slug)
	return render(request, "core/media.html", {'media': media})