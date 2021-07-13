import logging
import responses
import unittest
from crawler import Crawler


class TestCrawler(unittest.TestCase):

    def setUp(self) -> None:
        logging.disable(logging.CRITICAL)
        responses.add(
            responses.Response(
                method="GET",
                url="http://google.com",
                body='<a href="http://google.com">Test link</a>',
                status=200
            )
        )
        responses.add(
            responses.Response(
                method="GET",
                url="http://not.google.com",
                status=404
            )
        )
        self.empty_crawler = Crawler()

    @responses.activate
    def test_get_url_content_gets_html(self) -> None:
        url = "http://google.com"
        body = '<a href="http://google.com">Test link</a>'
        test_crawler = Crawler(url)
        res = test_crawler.get_url_content(url)

        self.assertEqual(res, body)

    def test_get_url_content_is_empty_for_invalid_url(self) -> None:
        url = "google.com"
        test_crawler = Crawler(url)
        res = test_crawler.get_url_content(url)

        self.assertEqual(res, "")

    @responses.activate
    def test_get_url_content_is_empty_for_invalid_status(self) -> None:
        url = "http://not.google.com"
        test_crawler = Crawler(url)
        res = test_crawler.get_url_content(url)

        self.assertEqual(res, "")

    def test_get_links_from_content_extracts_link_tags(self) -> None:
        content = """
        <div>
            <head> Test markup </head>
            <a href="https://google.com"></a>
            <a href="https://facebook.com"></a>
        </div>
        """
        expected = ["https://google.com", "https://facebook.com"]
        actual = self.empty_crawler.get_links_from_content(content)

        self.assertEqual(expected, actual)

    def test_get_links_from_content_returns_only_absolute_urls(self) -> None:
        content = """
        <div>
            <head> Test markup </head>
            <a href="https://google.com"></a>
            <a href="https://facebook.com"></a>
            <a href="/about"></a>
        </div>
        """
        expected = ["https://google.com", "https://facebook.com"]
        actual = self.empty_crawler.get_links_from_content(content)

        self.assertEqual(expected, actual)

    def test_get_links_from_content_is_empty_for_no_links(self) -> None:
        content = """
        <div>
            <head> Test markup </head>
        </div>
        """
        expected = []
        actual = self.empty_crawler.get_links_from_content(content)

        self.assertEqual(expected, actual)
