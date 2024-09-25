from django.db import models
from django.contrib.auth.models import User

from search.models import Tag


class Profile(models.Model):
	""" User account """
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	avatar = models.ImageField(default='user.png', upload_to='profile_images/%Y/%m/%d', blank=True)
	bio = models.TextField(max_length=1000, blank=True)
	tags = models.ManyToManyField(Tag, related_name='profiles', blank=True) # for searching
	following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)

	def __str__(self):
		return self.user.username

	def get_followers_count(self):
		return self.following.count()

	class Meta:
		verbose_name = "profile"
		verbose_name_plural = "profiles"