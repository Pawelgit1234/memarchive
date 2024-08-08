from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import NotFound

from .models import Playlist
from .serializers import PlaylistSerializer


class PlaylistListView(ListCreateAPIView):
    """List all playlists with pagination, or create a new playlist."""
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

    def create(self, request, *args, **kwargs):
        serializer = PlaylistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlaylistDetailView(RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a playlist."""
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

    def get_object(self):
        try:
            return super().get_object()
        except Playlist.DoesNotExist:
            raise NotFound()

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
