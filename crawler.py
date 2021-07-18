import logging
import requests
from bs4 import BeautifulSoup
from requests.models import MissingSchema
from typing import List


class Crawler:
    logging.basicConfig(format="[%(levelname)s] %(asctime)s: %(message)s")
    logger = logging.getLogger("Crawler")
    logger.setLevel(logging.DEBUG)

    def __init__(
        self,
        base_url: str = "",
        level: int = 0,
    ) -> None:
        """
        Args:
            base_url (str): base URL for this crawler
            level (int, optional): current level of this crawler.
            Defaults to 0.
            Use higher number for 'child' crawlers
        """
        self.level = level
        self.base_url = base_url

    def get_url_content(self, url: str) -> str:
        """Returns HTML content at URL if URL is valid and request is successful

        Args:
            url (str): URL to make request to

        Returns:
            str: HTML content of URL if request successful else empty
        """
        try:
            res = requests.get(url)
        except MissingSchema as ex:
            self.logger.warning(f"Invalid URL in get_url_content: {url}")
            self.logger.warning(ex)
            return ""
        # Don't let anti scrapping code, DNS, etc stop crawling
        except Exception as ex:
            self.logger.warning(f"Error getting content from {url}")
            self.logger.warning(ex)
            return ""
        if res.status_code != 200:
            self.logger.warning(
                f"Error in get_url_content for {url}: {res.status_code}"
            )
            return ""
        # Assume decoding is utf-8
        try:
            return res.content.decode("utf-8")
        except UnicodeDecodeError as ex:
            self.logger.warning(f"Invalid encoding while parsing {url}")
            self.logger.warning(ex)
            return ""

    def get_links_from_content(self, content: str) -> List[str]:
        """Extract non relative links from HTML content

        Args:
            content (str): HTML content

        Returns:
            List[str]: List of non relative links in HTML content
        """
        res: List[str] = []
        soup = BeautifulSoup(content, "lxml")
        for link in soup.find_all("a"):
            href: str = link.get("href")
            if self.is_valid_href(href):
                res.append(href)
        return res

    def is_valid_href(self, href: str) -> bool:
        """Check if link is a valid absolute link

        Args:
            href (str): URL to check

        Returns:
            bool: true if link is valid absolute link
        """
        return href and (href.startswith("http") or href.startswith("https"))

    def __str__(self):
        return f"Crawler: level: {self.level}, base_url: {self.base_url}"
