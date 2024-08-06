from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from .business import file_size, create_media_slug, media_file_validator, original_file_validator
from search.models import Tag


class Media(models.Model):
	""" Videos, Audios, Images, Gifs """
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medias', verbose_name='User')
	is_private = models.BooleanField('Is Private', default=False)
	title = models.CharField('Title', max_length=100)
	description = models.TextField('Description', max_length=1000, blank=True)
	text = models.TextField('Text', max_length=500, blank=True)
	media = models.FileField('Media', upload_to='media_files/%Y/%m/%d', validators=[media_file_validator, file_size])
	original = models.FileField('Original', upload_to='original_files/%Y/%m/%d', validators=[original_file_validator, file_size], blank=True, null=True)
	slug = models.SlugField('Slug', max_length=10, blank=True)
	timestamp = models.DateTimeField('Timestamp', default=timezone.now, blank=True)
	downloads_count = models.IntegerField('Downloads count', default=0)
	tags = models.ManyToManyField(Tag, related_name='medias', blank=True)

	def save(self, *args, **kwargs):
		self.slug = create_media_slug(self.title, self.media, self.user.username, str(self.timestamp))
		super().save(*args, **kwargs)

	def __str__(self):
		return self.title

	def get_likes_count(self):
		return self.likes.count()

	def get_views_count(self):
		return self.views.count()

	class Meta:
		verbose_name = "media"
		verbose_name_plural = "medias"


class MediaView(models.Model):
	""" If user see a media """
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='views', blank=True, null=True)
	media = models.ForeignKey(Media, on_delete=models.CASCADE, related_name='views')
	timestamp = models.DateTimeField("Timestamp", default=timezone.now)

	def __str__(self):
		return f"{self.user.username} - {self.media.title}"

	class Meta:
		verbose_name = "view"
		verbose_name_plural = "views"


class MediaLike(models.Model):
	""" If user like a media """
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
	media = models.ForeignKey(Media, on_delete=models.CASCADE, related_name='likes')
	timestamp = models.DateTimeField("Timestamp", default=timezone.now)

	def __str__(self):
		return f"{self.user.username} - {self.media.title}"

	class Meta:
		verbose_name = "like"
		verbose_name_plural = "likes"
		unique_together = ('media', 'user')
