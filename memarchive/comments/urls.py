from django.urls import path

from . import views

urlpatterns = [
	path('', views.CommentListView.as_view(), name='comment_list'),
	path('<int:pk>/', views.CommentDetailView.as_view(), name='comment_detail'),
	path('<int:pk>/like/', views.CommentLikeView.as_view(), name='comment_like'),
]


