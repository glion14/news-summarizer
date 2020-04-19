from unittest import TestCase

from summarize_news import Summarizer


class TestSummarizer(TestCase):

    def test_meaningcloud_api_key_not_empty(self):
        summarizer = Summarizer(number_of_sentences=5)
        self.assertTrue(summarizer.get_license_key() is not None)

    def test_summarize_text_from_url(self):
        arma_model_wiki = "https://en.wikipedia.org/wiki/Autoregressive%E2%80%93moving-average_model"
        summarizer = Summarizer(number_of_sentences=5)
        response = summarizer.summarize_text_from_url(url=arma_model_wiki)
        summary = response["summary"]
        self.assertIn("series", summary)
        self.assertIn("time", summary)
        self.assertIn("autoregression", summary)

    def test_summarize_text(self):
        """Text from https://www.bbc.com/news/world-us-canada-52330531"""
        with open('fixture/bbcnews.txt', 'r') as file:
            data = file.read()
            summarizer = Summarizer(number_of_sentences=5)
            response = summarizer.summarize_text(text=data)
            self.assertTrue(response is not None)
