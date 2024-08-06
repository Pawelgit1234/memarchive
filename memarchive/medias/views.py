from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser

from .models import Media, MediaLike, MediaView
from .serializers import MediaSerializer, MediaLikeSerializer, MediaViewSerializer


@csrf_exempt
def media_list(request):
    """ List all media, or create a new media """
    if request.method == 'GET':
        medias = Media.objects.all()
        serializer = MediaSerializer(medias, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MediaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def media_detail(request, pk):
    """ Retrieve, update or delete a media """
    try:
        media = Media.objects.get(pk=pk)
    except Media.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = MediaSerializer(media)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = MediaSerializer(media, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        media.delete()
        return HttpResponse(status=204)


@csrf_exempt
def media_like(request, pk):
    """ Like or unlike a media """
    try:
        media = Media.objects.get(pk=pk)
    except Media.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        data['media'] = media.id
        data['user'] = request.user.id
        serializer = MediaLikeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        try:
            like = MediaLike.objects.get(media=media, user=request.user)
            like.delete()
            return HttpResponse(status=204)
        except MediaLike.DoesNotExist:
            return HttpResponse(status=404)



@csrf_exempt
def media_view(request, pk):
    """ Give a view to a media """
    try:
        media = Media.objects.get(pk=pk)
    except Media.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        data['media'] = media.id
        data['user'] = request.user.id
        serializer = MediaViewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
