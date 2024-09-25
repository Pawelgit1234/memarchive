from django.urls import path

from . import views

urlpatterns = [
	path('follow/<int:pk>/', views.FollowProfileView.as_view(), name='profile_follow'),
]


