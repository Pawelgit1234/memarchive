from django.urls import path

from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('<slug:slug>/', views.media, name='media'),
]


