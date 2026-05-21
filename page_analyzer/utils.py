from urllib.parse import urlparse, urlunparse

def normalize_url(url):
    url = url.strip()
    parsed = urlparse(url)
    if not parsed.scheme and not parsed.netloc and parsed.path:
        parsed = urlparse(f"http://{url}")
    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()
    return f"{scheme}://{netloc}"