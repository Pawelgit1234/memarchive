from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

import os
import hashlib


def validate_file_extension(valid_extensions):
	def validator(value):
		ext = os.path.splitext(value.name)[1]  # Get the file extension
		if ext.lower() not in valid_extensions:
			raise ValidationError(_('Unsupported file extension. Allowed extensions are: {}').format(', '.join(valid_extensions)))
	return validator


def file_size(value):
	limit = 10 * 1024 * 1024  # 10 MB
	if value.size > limit:
		raise ValidationError(_('File too large. Size should not exceed 10 MB.'))


def create_media_slug(title: str, media_path: str, username: str, date: str) -> str:
	m = hashlib.sha256()
	m.update(title.encode())

	try:
		with open(media_path, 'rb') as media:
			for chunk in iter(lambda: media.read(4096), b""):
				m.update(chunk)
	except FileNotFoundError:
		raise ValidationError(f"Media file {media_path} not found.")

	m.update(username.encode())
	m.update(date.encode())

	return m.hexdigest()[:10]
