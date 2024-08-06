from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser

from .models import Comment, CommentLike
from .serializers import CommentSerializer, CommentLikeSerializer


@csrf_exempt
def comment_list(request):
	""" List of all comments, or create new comment """
	if request.method == 'GET':
		comments = Comment.objects.all()
		serializer = CommentSerializer(comments, many=True)
		return JsonResponse(serializer.data, safe=False)
	elif request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = CommentSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def comment_detail(request, pk):
	""" Retrieve, update or delete a comment """
	try:
		comment = Comment.objects.get(pk=pk)
	except Comment.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = CommentSerializer(comment)
		return JsonResponse(serializer.data)
	elif request.method == 'PUT':
		data = JSONParser().parse(request)
		serializer = CommentSerializer(comment, data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data)
		return JsonResponse(serializer.errors, status=400)
	elif request.method == 'DELETE':
		comment.delete()
		return HttpResponse(status=204)


@csrf_exempt
def comment_like(request, pk):
	""" Like or unlike a comment """
	try:
		comment = Comment.objects.get(pk=pk)
	except Comment.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'POST':
		data = JSONParser().parse(request)
		data['comment'] = comment.id
		serializer = CommentLikeSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)
	elif request.method == 'DELETE':
		try:
			like = CommentLike.objects.get(comment=comment, user=request.user)
			like.delete()
			return HttpResponse(status=204)
		except CommentLike.DoesNotExist:
			return HttpResponse(status=404)