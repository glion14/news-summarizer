from typing import List

from news_scraper import ReutersScraper, NewsApiPoller
from dataclasses import dataclass
from summarize_news import Summarizer
import smtplib


@dataclass
class NewsItem:
    url: str
    title: str
    summary: str

    def __str__(self) -> str:
        html = "<h2>" + self.title + "</h2>" + "<p>" + self.url + "</p>" + "<p>\n" + self.summary + "\n</p>"
        return html


def gcp_pubsub(event, context):
    urls = get_urls()
    all_news = summarize_content(urls=urls)
    send_mails(all_news=all_news)


def get_urls() -> List[str]:
    newsapi = NewsApiPoller()
    reuters_urls = newsapi.get_reuters_urls()
    return reuters_urls


def summarize_content(urls) -> List[NewsItem]:
    """" Scrapes the content. """
    summarizer = Summarizer(number_of_sentences=5)
    all_news = []

    for url in urls:
        reuters_scape = ReutersScraper(url=url)
        title, article = reuters_scape.reuters_news()
        summary = summarizer.summarize_text(text=article)["summary"]
        all_news.append(NewsItem(url=url, title=title, summary=summary))

    return all_news


def send_mails(all_news: List[NewsItem]):
    """ WIP: Creates a final message and sends it through mail.  """
    sender = 'glion14dev@gmail.com'
    receivers = ['amarksfeld@gmail.com']
    all_news_string = list(map(lambda x: str(x), all_news))
    message = '\n\n'.join(all_news_string)
    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sender, receivers, message)
    except smtplib.SMTPException:
        print("Error: unable to send email")