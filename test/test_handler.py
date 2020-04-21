from unittest import TestCase
import handler
from pprint import pprint


class Test(TestCase):
    def test_summarize_content(self):
        urls = [
            'http://feeds.reuters.com/~r/reuters/topNews/~3/mk1acjB40YU/canada-police-arrest-suspected-gunman-say-there-have-been-several-victims-idUSKBN2210KO',
            'http://feeds.reuters.com/~r/reuters/topNews/~3/0Y9eMGcM7AA/as-coronavirus-cases-rise-in-u-s-hot-spots-governors-tell-trump-its-too-soon-to-reopen-america-idUSKBN2210MH',
            'http://feeds.reuters.com/~r/reuters/topNews/~3/KqMQcZVTdR0/a-holy-land-easter-season-like-no-other-under-the-shadow-of-coronavirus-idUSKBN2210IK']
        all_news = handler.summarize_content(urls)
        pprint(all_news)
        self.assertEqual(len(urls), len(all_news))
