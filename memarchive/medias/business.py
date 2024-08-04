from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.files.storage import default_storage
from django.db import models

import os
import hashlib


def validate_file_extension(value, valid_extensions):
	ext = os.path.splitext(value.name)[1]  # Get the file extension
	if ext.lower() not in valid_extensions:
		raise ValidationError(_('Unsupported file extension. Allowed extensions are: {}').format(', '.join(valid_extensions)))


def media_file_validator(value):
	valid_extensions = ['.mp4', '.mp3', '.jpg', '.png', '.gif']
	validate_file_extension(value, valid_extensions)


def original_file_validator(value):
	valid_extensions = ['.rar', '.zip', '.7z']
	validate_file_extension(value, valid_extensions)


def file_size(value):
	limit = 10 * 1024 * 1024  # 10 MB
	if value.size > limit:
		raise ValidationError(_('File too large. Size should not exceed 10 MB.'))


def create_media_slug(title: str, media: models.FileField, username: str, date: str) -> str:
	file_path = default_storage.save(media.name, media)

	m = hashlib.sha256()
	with open(default_storage.path(file_path), 'rb') as media_file:
		for chunk in iter(lambda: media_file.read(4096), b""):
			m.update(chunk)

	m.update(title.encode())
	m.update(username.encode())
	m.update(date.encode())

	return m.hexdigest()[:10]
