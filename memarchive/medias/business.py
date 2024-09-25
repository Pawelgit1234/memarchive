from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.files.storage import default_storage
from django.utils import timezone

import os
import hashlib
from datetime import timedelta


def validate_file_extension(value, valid_extensions):
	ext = os.path.splitext(value.name)[1]  # Get the file extension
	if ext.lower() not in valid_extensions:
		raise ValidationError(_('Unsupported file extension. Allowed extensions are: {}').format(', '.join(valid_extensions)))


def media_file_validator(value):
	valid_extensions = ['.mp4', '.mp3', '.wav', '.jpg', '.png', '.gif']
	validate_file_extension(value, valid_extensions)


def original_file_validator(value):
	valid_extensions = ['.rar', '.zip', '.7z']
	validate_file_extension(value, valid_extensions)


def file_size(value):
	limit = 10 * 1024 * 1024  # 10 MB
	if value.size > limit:
		raise ValidationError(_('File too large. Size should not exceed 10 MB.'))


def create_media_slug(title: str, media, username: str, date: str) -> str:
	file_path = default_storage.save(media.name, media)

	m = hashlib.sha256()
	with open(default_storage.path(file_path), 'rb') as media_file:
		for chunk in iter(lambda: media_file.read(4096), b""):
			m.update(chunk)

	m.update(title.encode())
	m.update(username.encode())
	m.update(date.encode())

	return m.hexdigest()[:10]


def add_view(media_id, user_id) -> bool:
	""" Add a view to a media with a check for repeated views within the last hour """
	from .models import Media, MediaView

	try:
		media = Media.objects.get(pk=media_id)
		user = User.objects.get(pk=user_id)
	except Media.DoesNotExist:
		raise ValueError("Media not found")
	except User.DoesNotExist:
		raise ValueError("User not found")

	one_hour_ago = timezone.now() - timedelta(hours=1)

	if MediaView.objects.filter(media=media, user=user, timestamp__gte=one_hour_ago).exists():
		return False

	MediaView.objects.create(media=media, user=user)
	return True
