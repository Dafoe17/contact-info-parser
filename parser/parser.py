from parser.crawler import SiteCrawler


class SiteContactParser:

    def __init__(self, start_url: str):
        self.start_url = start_url
        self._crawler = SiteCrawler(start_url)

    def parse(self) -> dict:
        result = self._crawler.crawl()
        return result
