import os
from typing import List, Tuple
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
    urls, bulgarian_urls = get_urls()
    all_news = summarize_content(urls=urls)
    send_mails(all_news=all_news, non_summarized_urls=bulgarian_urls)
    return "Done!"


def get_urls() -> Tuple[List[str], List[Tuple[str, str, str]]]:
    newsapi = NewsApiPoller()
    reuters_urls = newsapi.get_reuters_urls()
    bulgarian_urls = newsapi.get_bulgarian_urls()
    return reuters_urls, bulgarian_urls


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


def send_mails(all_news: List[NewsItem], non_summarized_urls: List[Tuple[str, str, str]]):
    """ WIP: Creates a final message and sends it through mail.  """
    SENDER = "Sender Name <glion14dev@gmail.com>"
    RECIPIENT = os.environ["EMAIL_RECIPIENTS"].split(",")
    SUBJECT = "Summarized news " + str(datetime.datetime.now().date())
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

    for (url, title, description) in non_summarized_urls:
        BODY_HTML += """
            <h2 style="color: #2e6c80;">{title}</h2>
            <p>{description}</p>
            <a href='{url}'>Non-summarized news</a>
            <br><br>
        """.format(url=url, title=title, description=description)

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
