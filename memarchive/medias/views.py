from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import NotFound

from .models import Media, MediaLike, MediaView
from .serializers import MediaSerializer, MediaLikeSerializer, MediaViewSerializer


class MediaListView(ListAPIView):
    """ List all media with pagination, or create a new media """
    queryset = Media.objects.all()
    serializer_class = MediaSerializer

    def post(self, request, *args, **kwargs):
        serializer = MediaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MediaDetailView(RetrieveUpdateDestroyAPIView):
    """ Retrieve, update or delete a media """
    queryset = Media.objects.all()
    serializer_class = MediaSerializer


class MediaLikeView(ListAPIView):
    """ Like or unlike a media """
    def get_object(self, pk):
        try:
            return Media.objects.get(pk=pk)
        except Media.DoesNotExist:
            raise NotFound()

    def post(self, request, pk):
        """ add like """
        media = self.get_object(pk)
        user = request.user

        if MediaLike.objects.filter(media=media, user=user).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        like = MediaLike.objects.create(media=media, user=user)
        return Response({'liked': True, 'likes_count': media.get_likes_count()}, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        """ delete like """
        media = self.get_object(pk)
        try:
            like = MediaLike.objects.get(media=media, user=request.user)
            like.delete()
            return Response({'liked': False, 'likes_count': media.get_likes_count()}, status=status.HTTP_200_OK)
        except MediaLike.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class MediaViewView(ListAPIView):
    """ Give a view to a media """
    def get_object(self, pk):
        try:
            return Media.objects.get(pk=pk)
        except Media.DoesNotExist:
            raise NotFound()

    def post(self, request, pk):
        media = self.get_object(pk)
        data = request.data
        data['media'] = media.id
        data['user'] = request.user.id
        serializer = MediaViewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
