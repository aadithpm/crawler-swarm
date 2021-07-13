Concurrent web crawler in Python 3. Powered by `BeautifulSoup` and `requests`. Crawls a website for all non-relative links and queues those links for further crawling until a user-defined 'level' of crawling is reached (or you get bored of waiting for the crawler to finish).

## Setup:

- Clone repo locally: `git clone REPO_URL`
- **Optional:** Create a virtual environment: `python -m venv env`
- Install requirements: `pip install -r requirements.txt`

- Running unittests: `python -m unittest`
- Running the crawler:
```
python crawler.py [--help] --url=URL --levels=LEVELS

help - displays help message
url - URL to crawl
levels - maximum levels to crawl from starting URL
```

### Improvements:

- Visit only unique links
    - For 'parent' and 'child' links, do not visit a link that has already been visited. For example, social links are available on every page of a company's website. Resources are wasted by queueing these for crawling when they will be a part of the crawl queue on the first instance anyway

- Present links on a different interface
    - A console application is the fastest to develop but a web application might present this information in a more organized and navigable format

