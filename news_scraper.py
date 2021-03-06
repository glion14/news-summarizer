import os
from typing import List, Tuple

import requests
from bs4 import BeautifulSoup
from newsapi import NewsApiClient


class Scraper(object):
    def __init__(self, url) -> None:
        super().__init__()
        self.url = url

    def get_soup_from_url(self) -> BeautifulSoup:
        response = requests.get(url=self.url)
        return BeautifulSoup(response.content, 'html.parser')


class ReutersScraper(Scraper):

    def __init__(self, url="") -> None:
        super().__init__(url)

    def reuters_news(self) -> [str, str]:
        """ Parses a title and article text from the news. Article text is trimmed by the Reuters prefix. """
        soup = self.get_soup_from_url()
        title = soup.title.string.strip()
        full_article = soup.find(name="div", attrs={"class": "StandardArticleBody_body"}).text
        return title, full_article


class AktualityScraper(Scraper):

    def __init__(self, url) -> None:
        super().__init__(url)

    def aktuality_news(self) -> [str, str, str]:
        soup = self.get_soup_from_url()
        head = soup.title.string
        perex = soup.find(name="div", attrs={"class": "introtext", "id": "perex-id"}).text
        body = soup.find(name="div", attrs={"class": "fulltext", "id": "content-id"}).text
        return head, perex, body


class NewsApiPoller(object):

    def __init__(self) -> None:
        super().__init__()
        self._news_api_key = os.environ["NEWSAPI_KEY"]
        self._api = NewsApiClient(self._news_api_key)

    def get_aktuality_urls(self) -> List[str]:
        result = self._api.get_top_headlines(country="sk")
        aktuality_filtered_articles = list(filter(lambda x: x['source']['name'] == 'Aktuality.sk', result['articles']))
        aktuality_articles_urls = list(map(lambda x: x["url"], aktuality_filtered_articles))
        return aktuality_articles_urls

    def get_reuters_urls(self) -> List[str]:
        result = self._api.get_top_headlines(sources="reuters")
        reuters_urls = list(map(lambda x: x["url"], result['articles']))
        return reuters_urls

    def get_bulgarian_urls(self) -> List[Tuple[str, str, str]]:
        result = self._api.get_top_headlines(country="bg")
        bulgarian_news = list(map(lambda x: (x["url"], x["title"], x["description"]), result["articles"]))
        return bulgarian_news