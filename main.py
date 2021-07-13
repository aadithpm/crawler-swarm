import argparse
import logging
import sys
from constants import HELP_MESSAGE
from crawler_swarm import CrawlerSwarm
from crawler import Crawler
from rich import print


def main() -> None:
    logging.basicConfig(format="[%(levelname)s] %(asctime)s: %(message)s")
    logger = logging.getLogger("Main")
    logger.setLevel(logging.DEBUG)
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--help", action='store_true')
    parser.add_argument("--url", type=str)
    parser.add_argument("--levels", type=int)
    args = vars(parser.parse_args())
    help_flag, url, levels = args['help'], args['url'], args['levels']

    if help_flag:
        print(HELP_MESSAGE)
        sys.exit(2)

    if url:
        crawler = Crawler(url) if not levels else Crawler(url, levels)
        crawler_swarm = CrawlerSwarm([crawler])
        crawler_swarm.process_crawlers()
        sys.exit(0)

    else:
        print("[bold] Invalid usage [/bold]")
        print(HELP_MESSAGE)
        sys.exit(2)


if __name__ == "__main__":
    main()
