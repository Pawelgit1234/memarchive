from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from media.models import Media


class Comment(models.Model):
	""" For commenting medias """

	content = models.TextField('Content', max_length=500)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='User')
	media = models.ForeignKey(Media, on_delete=models.CASCADE, related_name='comments')
	parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies', verbose_name='Parent Comment')
	timestamp = models.DateTimeField("Timestamp", default=timezone.now)

	def __str__(self):
		return f"{self.user.username} - {self.content[:10]}"

	class Meta:
		verbose_name = "comment"
		verbose_name_plural = "comments"


class CommentLike(models.Model):
	""" If user like a media """
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_likes')
	comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_likes')
	timestamp = models.DateTimeField("Timestamp", default=timezone.now)

	def __str__(self):
		return f"{self.user.username} - {self.comment.content[:10]}"

	class Meta:
		verbose_name = "comment_like"
		verbose_name_plural = "comment_likes"
		unique_together = ('comment', 'user')