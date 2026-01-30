import requests
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
from collections import deque
from typing import Set
import urllib.robotparser

from parser.utils.config import config
from parser.utils.logger import logger
from parser.url_handler import (
    normalize_url,
    extract_domain,
    build_absolute_url,
    is_same_domain,
    is_valid_link,
)
from parser.extractor import ContactExtractor
import warnings


warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)


class SiteCrawler:
    def __init__(self, start_url: str):
        self.start_url = normalize_url(start_url)
        if self.start_url is None:
            logger.error("Некорректный URL: %s", start_url)
            raise ValueError(f"Некорректный URL: {start_url}")
        
        self.rp = urllib.robotparser.RobotFileParser()
        self.rp.set_url(f"{self.start_url}/robots.txt")
        try:
            self.rp.read()
        except:
            logger.warning("Не удалось прочитать robots.txt")
            self.rp = None


        self.base_domain = extract_domain(self.start_url)

        self.visited_urls: Set[str] = set()
        self.emails: Set[str] = set()
        self.phones: Set[str] = set()

    def crawl(self) -> dict:
        logger.info("Начинаем обход сайта: %s", self.start_url)

        queue = deque()
        queue.append((self.start_url, 0))

        while queue and len(self.visited_urls) < config.max_pages:
            current_url, depth = queue.popleft()

            if depth > config.max_depth:
                continue

            if current_url in self.visited_urls:
                continue

            if self.rp and not self.rp.can_fetch("*", current_url):
                logger.info("Пропускаем %s из-за robots.txt", current_url)
                continue


            logger.info("Посещаем страницу: %s", current_url)
            self.visited_urls.add(current_url)

            html = self._fetch_page(current_url)
            if not html:
                continue

            self._extract_contacts(html)

            links = self._extract_links(html, current_url)

            for link in links:
                if (
                    link not in self.visited_urls
                    and is_same_domain(link, self.base_domain)
                ):
                    queue.append((link, depth + 1))

        logger.info("Обход завершен: %s страниц", len(self.visited_urls))
        logger.info("Emails найдено: %s, телефонов: %s", len(self.emails), len(self.phones))


        return {
            "url": self.start_url,
            "emails": sorted(self.emails),
            "phones": sorted(self.phones),
        }

    def _fetch_page(self, url: str) -> str | None:
        for attempt in range(3):
            try:
                response = requests.get(
                    url,
                    timeout=config.request_timeout,
                    headers={"User-Agent": config.user_agent},
                )

                if response.status_code != 200:
                    logger.warning("Ошибка ответа %s для %s", response.status_code, url)
                    return None

                return response.text

            except requests.RequestException as e:
                logger.warning("Ошибка запроса %s для %s: %s", attempt+1, url, e)
        return None

    def _extract_contacts(self, html: str) -> None:

        soup = BeautifulSoup(html, "html.parser")

        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        text = soup.get_text(separator=" ")

        emails = ContactExtractor.extract_emails(text)
        phones = ContactExtractor.extract_phones(text)

        if emails:
            logger.debug("Найдены email: %s", emails)

        if phones:
            logger.debug("Найдены телефоны: %s", phones)

        self.emails.update(emails)
        self.phones.update(phones)

    def _extract_links(self, html: str, base_url: str) -> Set[str]:

        soup = BeautifulSoup(html, "html.parser")
        links = set()

        for tag in soup.find_all("a", href=True):
            href_value = tag.get("href")
            if not href_value:
                continue

            href_str = str(href_value)
            absolute_url = build_absolute_url(base_url, href_str)

            if not is_valid_link(absolute_url):
                continue

            links.add(absolute_url)

        return links
