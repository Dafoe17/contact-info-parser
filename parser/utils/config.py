from dataclasses import dataclass


@dataclass(frozen=True)
class ParserConfig:
    max_pages: int = 50
    max_depth: int = 3
    request_timeout: int = 5
    user_agent: str = (
        "Mozilla/5.0 (compatible; SiteContactParser/1.0; +https://example.com/bot)"
    )
    allowed_schemes: tuple[str, ...] = ("http", "https")
    phone_region: str = "RU"

config = ParserConfig()
