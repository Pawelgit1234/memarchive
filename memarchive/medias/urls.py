from django.urls import path

from . import views

urlpatterns = [
	path('medias/', views.media_list, name='media_list'),
	path('medias/<int:pk>/', views.media_detail, name='media_detail'),
	path('medias/<int:pk>/like', views.media_like, name='media_like'),
	path('medias/<int:pk>/view', views.media_view, name='media_view'),
]


