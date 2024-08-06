from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser

from .models import Playlist
from .serializers import PlaylistSerializer

@csrf_exempt
def playlist_list(request):
	""" List all playlists, or create a new playlist """
	if request.method == 'GET':
		playlists = Playlist.objects.all()
		serializer = PlaylistSerializer(playlists, many=True)
		return JsonResponse(serializer.data, safe=False)
	elif request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = PlaylistSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def playlist_detail(request, pk):
	""" Retrieve, update or delete a playlist """
	try:
		playlist = Playlist.objects.get(pk=pk)
	except Playlist.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = PlaylistSerializer(playlist)
		return JsonResponse(serializer.data)
	elif request.method == 'PUT':
		data = JSONParser().parse(request)
		serializer = PlaylistSerializer(playlist, data=data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data)
		return JsonResponse(serializer.errors, status=400)
	elif request.method == 'DELETE':
		playlist.delete()
		return HttpResponse(status=204)