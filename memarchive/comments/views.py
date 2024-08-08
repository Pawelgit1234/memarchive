from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import NotFound

from .models import Comment, CommentLike
from .serializers import CommentSerializer, CommentLikeSerializer


class CommentListView(ListAPIView):
    """ List all comments with pagination, or create a new comment """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def post(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailView(RetrieveUpdateDestroyAPIView):
    """ Retrieve, update or delete a comment """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentLikeView(ListAPIView):
    """ Like or unlike a comment """
    def get_object(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise NotFound()

    def post(self, request, pk, *args, **kwargs):
        comment = self.get_object(pk)
        data = request.data
        data['comment'] = comment.id
        data['user'] = request.user.id
        serializer = CommentLikeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        comment = self.get_object(pk)
        try:
            like = CommentLike.objects.get(comment=comment, user=request.user)
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CommentLike.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
