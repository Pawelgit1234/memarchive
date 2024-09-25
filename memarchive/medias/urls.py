from django.urls import path

from . import views

urlpatterns = [
	path('', views.MediaListView.as_view(), name='media_list'),
	path('<int:pk>/', views.MediaDetailView.as_view(), name='media_detail'),
	path('like/<int:pk>/', views.MediaLikeView.as_view(), name='media_like'),
	path('view/<int:pk>/', views.MediaViewView.as_view(), name='media_view'),
]