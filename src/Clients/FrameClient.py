from bs4 import BeautifulSoup
from BaseWebClient import BaseWebClient


class CondorWebClient(BaseWebClient):
    def __init__(self, timeout = 10):
        super().__init__(timeout)

    def _parse(self, html):
        return super()._parse(html)