import hashlib


def create_playlist_slug(title: str, username: str, date: str) -> str:
	m = hashlib.sha256()
	m.update(title.encode())
	m.update(username.encode())
	m.update(date.encode())

	return m.hexdigest()[:10]