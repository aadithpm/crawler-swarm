import logging
import responses
import unittest
from crawler import Crawler
from crawler_swarm import CrawlerSwarm
from unittest.mock import MagicMock


class TestCrawlerSwarm(unittest.TestCase):

    def setUp(self) -> None:
        logging.disable(logging.CRITICAL)
        responses.add(
            responses.Response(
                method="GET",
                url="http://google.com",
                body='<a href="https://twitter.com">Test child link</a>',
                status=200
            )
        )
        responses.add(
            responses.Response(
                method="GET",
                url="http://twitter.com",
                body='<a href="/about/">Test child 2 link</a>',
                status=404
            )
        )
        self.crawler = Crawler("https://google.com")
        self.crawler_swarm = CrawlerSwarm(self.crawler)

    def test_add_crawlers_adds_to_swarm(self) -> None:
        crawler_swarm = CrawlerSwarm()
        crawler_swarm.add_crawlers([Crawler(), Crawler()])

        self.assertEqual(len(crawler_swarm.crawlers), 2)

    def test_add_crawlers_maintains_swarm_level_order(self) -> None:
        crawler_swarm = CrawlerSwarm([Crawler(level=3), Crawler(level=1)])
        crawler_swarm.add_crawlers(
            [
                Crawler(level=2),
                Crawler(level=1),
                Crawler(level=3),
                Crawler(level=1),
            ]
        )
        expected_levels = [1, 1, 1, 2, 3, 3]

        self.assertEqual(list(map(lambda x: x.level, crawler_swarm.crawlers)), expected_levels)

    def test_run_crawler_gets_content_and_parses_links(self) -> None:
        self.crawler.get_links_from_content = MagicMock()
        self.crawler.get_url_content = MagicMock()

        self.crawler_swarm.run_crawler(self.crawler)

        assert self.crawler.get_url_content.called
        assert self.crawler.get_links_from_content.called
