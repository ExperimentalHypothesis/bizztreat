import requests
from bs4 import BeautifulSoup

url = "https://www.bizztreat.com/bizztro?p1400=1"


class Parser:

    def __init__(self, url):
        self.page = requests.get(url).text
        self.soup = BeautifulSoup(self.page, "html.parser")

    @property
    def titles(self):
        locator = "h3.entry-title a"
        titles = [i["title"] for i in self.soup.select(locator)]
        return titles

    @property
    def urls(self):
        locator = "h3.entry-title a"
        urls = [i["href"] for i in self.soup.select(locator)]
        return urls

    @property
    def images(self):
        locator = "a.image img"
        images = []

        for i in self.soup.select(locator):
            if "src" in i.attrs and images[-1] != i["src"]:  # strange case needs strange condition
                images.append(i["src"])
            elif "data-srcset" in i.attrs:
                images.append(i["data-srcset"].split()[0])

        return images

    @property
    def summaries(self):
        locator = "p.entry-body__text"
        summaries = [i.text.strip() for i in self.soup.select(locator)]
        return summaries

