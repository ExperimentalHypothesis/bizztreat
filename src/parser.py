import requests
import logging
from collections import namedtuple
from bs4 import BeautifulSoup

logger = logging.getLogger("scape-bizz.parser")


class Parser:
    row = namedtuple("row", ["titles", "urls", "images", "summaries"])

    def __init__(self, url):
        self.url = url
        self.page = requests.get(url).text
        logger.debug(f"Parser created for page `{url}`")
        self.soup = BeautifulSoup(self.page, "html.parser")

    @property
    def titles(self):
        locator = "h3.entry-title a"
        logger.debug(f"Getting all titles using `{locator}`")
        titles = [i["title"] for i in self.soup.select(locator)]
        return titles

    @property
    def urls(self):
        locator = "h3.entry-title a"
        logger.debug(f"Getting all urls using `{locator}`")
        urls = [i["href"] for i in self.soup.select(locator)]
        return urls

    @property
    def images(self):
        locator = "a.image img"
        logger.debug(f"Getting all images using `{locator}`")

        images = []
        for i in self.soup.select(locator):
            # strange case, needs strange condition
            if "src" in i.attrs and i["src"] not in images:
                images.append(i["src"])
            # regular case
            elif "data-srcset" in i.attrs:
                images.append(i["data-srcset"].split()[0])

        return images

    @property
    def summaries(self):
        locator = "p.entry-body__text"
        logger.debug(f"Getting all summaries using `{locator}`")
        summaries = [i.text.strip() for i in self.soup.select(locator)]
        return summaries

    def parse(self) -> list[namedtuple]:
        logger.debug(f"Parsing started for page {self.url}")
        titles = self.titles
        urls = self.urls
        images = self.images
        summaries = self.summaries

        rows = []
        for i in zip(titles, urls, images, summaries, strict=True):
            r = self.row(*i)
            rows.append(r)

        logger.info(f"Parsed {len(rows)} rows from page {self.url}")
        return rows
