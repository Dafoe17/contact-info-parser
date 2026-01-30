from urllib.parse import urlparse, urljoin, urldefrag
from typing import Optional

from parser.utils.config import config


def normalize_url(url: str) -> Optional[str]:
    if not url:
        return None

    url, _ = urldefrag(url)
    parsed = urlparse(url)
    if parsed.scheme not in config.allowed_schemes:
        return None
    
    normalized = url.rstrip("/")

    return normalized


def is_same_domain(url: str, base_domain: str) -> bool:
    parsed = urlparse(url)
    return parsed.netloc == base_domain


def extract_domain(url: str) -> str:
    parsed = urlparse(url)
    return parsed.netloc


def build_absolute_url(base_url: str, link: str) -> Optional[str]:
    if not link:
        return None

    absolute_url = urljoin(base_url, link)
    return normalize_url(absolute_url)


def is_valid_link(url: Optional[str]) -> bool:
    if not url:
        return False

    parsed = urlparse(url)

    forbidden_extensions = (
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".pdf",
        ".zip",
        ".rar",
        ".doc",
        ".docx",
        ".xls",
        ".xlsx",
        ".ppt",
        ".pptx",
    )

    path = parsed.path.lower()
    if any(path.endswith(ext) for ext in forbidden_extensions):
        return False

    return True
