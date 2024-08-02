from django.db import models
from django.utils import timezone


class Tag(models.Model):
	""" Can be used by users and medias """
	name = models.CharField('Name', max_length=25)
	timestamp = models.DateTimeField('Timestamp', default=timezone.now)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "tag"
		verbose_name_plural = "tags"