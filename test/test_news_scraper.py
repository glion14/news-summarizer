from unittest import TestCase

import news_scraper


class ScraperTest(TestCase):
    # Test Reuters
    def test_get_reuters_news(self):
        reuterscraper = news_scraper.ReutersScraper(
            url="https://www.reuters.com/article/us-health-coronavirus-trump-china/trump-warns-china-could-face-consequences-for-virus-outbreak-idUSKBN2200XZ")
        head, text = reuterscraper.reuters_news()
        self.assertEqual("Trump warns China could face consequences for virus outbreak - Reuters", head)
        self.assertIn("Donald Trump", text)


    # Test Aktuality
    def test_scrape_aktuality_articles(self):
        aktualityscraper = news_scraper.AktualityScraper(
            url="https://www.aktuality.sk/clanok/783453/koronavirus-situacia-v-taliansku-sa-postupne-zlepsuje/")
        head, perex, body = aktualityscraper.aktuality_news()
        self.assertEqual("Koronavírus: Situácia v Taliansku sa postupne zlepšuje | Aktuality.sk", head)
        self.assertEqual("V Taliansku pribudlo 482 obetí, čo je oproti predchádzajúcemu dňu pokles.", perex)
        self.assertIn("COVID-19", body)


class NewsApiTest(TestCase):
    # Test News API
    def test_get_aktuality_urls(self):
        newsapi = news_scraper.NewsApiPoller()
        articles_urls = newsapi.get_aktuality_urls()
        map(lambda x: self.assertIn("aktuality.sk", x), articles_urls)

    def test_get_reuters_urls(self):
        newsapi = news_scraper.NewsApiPoller()
        article_urls = newsapi.get_reuters_urls()
        map(lambda x: self.assertIn("reuters", x), article_urls)
