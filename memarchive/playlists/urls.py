from django.urls import path

from . import views

urlpatterns = [
	path('playlists/', views.playlist_list, name='playlist_list'),
	path('playlists/<int:pk>/', views.playlist_detail, name='playlist_detail'),
]


