import os
from typing import List
import datetime

import boto3
from botocore.exceptions import ClientError

from news_scraper import ReutersScraper, NewsApiPoller
from summarize_news import Summarizer


class NewsItem:
    url: str
    title: str
    summary: str

    def __init__(self, url, title, summary) -> None:
        super().__init__()
        self.url = url
        self.title = title
        self.summary = summary

    def __str__(self) -> str:
        html = "<h2>" + self.title + "</h2>" + "<p>" + self.url + "</p>" + "<p>\n" + self.summary + "\n</p>"
        return html


def lambda_handler(event, context):
    urls = get_urls()
    all_news = summarize_content(urls=urls)
    send_mails(all_news=all_news)
    return "Done!"


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
    SENDER = "Sender Name <glion14dev@gmail.com>"
    RECIPIENT = os.environ["EMAIL_RECIPIENTS"].split(",")
    SUBJECT = "Summarized news " + str(datetime.datetime.now().date())
    all_news_string = list(map(lambda x: str(x), all_news))
    AWS_REGION = os.environ['AWS_REGION']
    CHARSET = "UTF-8"

    BODY_HTML = """<html>
    <head></head>
    <body>
      <h1 style="color: #5e9ca0;">Your daily digest of summarized news</h1>
    """
    for news in all_news:
        BODY_HTML += """
            <h2 style="color: #2e6c80;">{title}</h2>
            <a href='{url}'>Link</a>
            <p>{summary}</p><br><br>
        """.format(title=news.title, url=news.url, summary=news.summary)

    BODY_HTML += """
    </body>
    </html>"""

    client = boto3.client('ses', region_name=AWS_REGION)
    try:
        response = client.send_email(
            Destination={
                'ToAddresses': RECIPIENT,
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
