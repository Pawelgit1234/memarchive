from django.urls import path

from . import views

urlpatterns = [
	path('', views.PlaylistListView.as_view(), name='playlist_list'),
	path('<int:pk>/', views.PlaylistDetailView.as_view(), name='playlist_detail'),
]


