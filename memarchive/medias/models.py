from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from .business import validate_file_extension, file_size, create_slug


class Media(models.Model):
	""" Videos, Audios, Images, Gifs """
	valid_media_extensions = ['.mp4', '.mp3', '.jpg', '.png', '.gif']
	valid_original_extensions = ['.rar', '.zip', '.7z']

	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medias', verbose_name='User')
	title = models.CharField('Title', max_length=100)
	description = models.TextField('Description', max_length=1000, blank=True)
	text = models.TextField('Text', max_length=500, blank=True)
	media = models.FileField('Media', upload_to='media_files/%Y/%m/%d', validators=[validate_file_extension(valid_media_extensions), file_size])
	original = models.FileField('Original', upload_to='original_files/%Y/%m/%d', validators=[validate_file_extension(valid_original_extensions), file_size], blank=True, null=True)
	slug = models.SlugField('Slug', max_length=10, blank=True)
	timestamp = models.DateTimeField('Timestamp', default=timezone.now, blank=True)
	downloads_count = models.IntegerField('Downloads count', default=0)
	tags = ...

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = create_slug(self.title, self.media.path, self.user.username, str(self.date))
		super(Media, self).save(*args, **kwargs)

	def __str__(self):
		return self.title

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
