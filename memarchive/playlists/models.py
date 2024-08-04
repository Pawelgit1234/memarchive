from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from medias.models import Media
from .business import create_playlist_slug


class Playlist(models.Model):
	""" Users can save medias in playlists """

	title = models.CharField('Title', max_length=20)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists', verbose_name='User')
	timestamp = models.DateTimeField('Timestamp', default=timezone.now, blank=True)
	slug = models.SlugField('Slug', max_length=10, blank=True)
	medias = models.ManyToManyField(Media, related_name='playlists', verbose_name='Medias')

	def save(self, *argc, **kwargs):
		self.slug = create_playlist_slug(self.title, self.user.username, str(self.timestamp))
		super().save(*argc, **kwargs)

	def __str__(self):
		return self.title

	def media_count(self):
		return self.medias.count()

	media_count.short_description = 'Media Count'

	class Meta:
		verbose_name = "playlist"
		verbose_name_plural = "playlists"
