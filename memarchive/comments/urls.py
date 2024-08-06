from django.urls import path

from . import views

urlpatterns = [
	path('comments/', views.comment_list, name='comment_list'),
	path('comments/<int:pk>/', views.comment_detail, name='comment_detail'),
	path('comments/<int:pk>/like/', views.comment_like, name='comment_like'),
]


