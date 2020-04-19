import requests
import os


class Summarizer:
    def __init__(self, number_of_sentences):
        self._licensekey = os.getenv("MEANINGCLOUD_API_KEY")
        self._api_url = "https://api.meaningcloud.com/summarization-1.0"
        self._number_of_sentences = number_of_sentences

    def summarize_text_from_url(self, url: str) -> dict:
        """ Creates a summarization of text in a given URL. """
        post_req_data = {"key": self._licensekey,
                         "of": "json",
                         "url": url,
                         "sentences": self._number_of_sentences
                         }
        return requests.post(url=self._api_url, data=post_req_data).json()

    def summarize_text(self, text: str) -> dict:
        """ Creates a summarization of given text. """
        post_req_data = {"key": self._licensekey,
                         "of": "json",
                         "txt": text,
                         "sentences": self._number_of_sentences
                         }
        return requests.post(url=self._api_url, data=post_req_data).json()

    def get_license_key(self) -> str:
        return self._licensekey