import concurrent.futures
import logging
from constants import DEFAULT_CRAWLER_MAX_LEVEL, OUTPUT_NESTING_FACTOR
from crawler import Crawler
from rich import print
from typing import List


class CrawlerSwarm:
    logging.basicConfig(format="[%(levelname)s] %(asctime)s: %(message)s")
    logger = logging.getLogger("CrawlerSwarm")
    logger.setLevel(logging.DEBUG)

    def __init__(
        self,
        crawlers: List[Crawler] = [],
        max_level: int = DEFAULT_CRAWLER_MAX_LEVEL
    ) -> None:
        """
        Args:
            crawlers (List[Crawler], optional): List of crawlers in this swarm.
            Defaults to [].
            max_level (int, optional): Max link levels to explore.
            Defaults to DEFAULT_CRAWLER_MAX_LEVEL.
        """
        self.crawlers = crawlers
        self.max_level = max_level

    def __add_crawler__(self, crawler: Crawler) -> None:
        """Adds crawler to the swarm

        Args:
            crawler (Crawler)
        """
        self.crawlers.append(crawler)

    def __sort_crawlers__(self) -> None:
        """Maintains order in the swarm's Crawlers"""
        self.crawlers.sort(key=lambda x: x.level)

    def add_crawlers(self, crawlers: List[Crawler]) -> None:
        """Adds crawlers and sorts the crawler list in the swarm

        Args:
            crawlers (List[Crawler])
        """
        for crawler in crawlers:
            self.__add_crawler__(crawler)
        self.__sort_crawlers__()

    def run_crawler(self, crawler: Crawler) -> List[Crawler]:
        """Runs a crawler, logs the result
        and returns child crawlers for its links

        Args:
            crawler (Crawler): crawler to run

        Returns:
            List[Crawler]: child crawlers for links in this crawler's page
        """
        res = []
        child_crawler_level = crawler.level + 1
        content = crawler.get_url_content(crawler.base_url)
        if content:
            links = crawler.get_links_from_content(content)
            print(f"{' ' * crawler.level * OUTPUT_NESTING_FACTOR} [bold]{crawler.base_url}[/bold]")
            for link in links:
                print(f"{' ' * crawler.level * OUTPUT_NESTING_FACTOR} [grey82]{[crawler.level]} - {link}[/grey82]")
                # Stopping condition for crawling
                if child_crawler_level <= self.max_level:
                    res.append(
                        Crawler(
                            base_url=link,
                            level=child_crawler_level
                        )
                    )
        return res

    def process_crawlers(self) -> None:
        """Asynchronously runs crawler to get links, creates child crawlers
        and adds them to the swarm
        """
        while self.crawlers:
            # Collect crawlers to run and clear current queue
            crawlers_to_run = self.crawlers[:]
            self.crawlers.clear()
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=5
            ) as executor:
                for crawler in crawlers_to_run:
                    future = executor.submit(self.run_crawler, crawler)
                    child_crawlers = future.result()
                    self.add_crawlers(child_crawlers)
