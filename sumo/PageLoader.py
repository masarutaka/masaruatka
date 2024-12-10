import requests
from bs4 import BeautifulSoup
from retry import retry

class PageLoader:
    def __init__(self, base_url):
        self.base_url = base_url

    @retry(tries=3, delay=10, backoff=2)
    def load_page(self, page):
        """ページを読み込んでBeautifulSoupオブジェクトを返す"""
        url = self.base_url.format(page)
        response = requests.get(url)
        response.raise_for_status()  # HTTPエラーをチェック
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup

