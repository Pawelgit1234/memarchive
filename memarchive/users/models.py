from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
	""" User account """
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	avatar = models.ImageField(default='user.png', upload_to='profile_images/%Y/%m/%d')
	bio = models.TextField(max_length=1000, blank=True)

	def __str__(self):
		self.user.username

	class Meta:
		verbose_name = "profile"
		verbose_name_plural = "profiles"