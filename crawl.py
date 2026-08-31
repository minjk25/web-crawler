from urllib.parse import urlsplit


def normalize_url(url: str) -> str:
    parsed_url = urlsplit(url)
    return f"{parsed_url.hostname}{parsed_url.path}".rstrip("/")
