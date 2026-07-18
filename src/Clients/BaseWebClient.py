import requests as re
from requests import Session
from abc import ABC, abstractmethod
from DTOs.PriceDTO import PriceDTO

class BaseWebClient(ABC):
    def __init__(self, timeout: int = 10) -> None:
        self.session = re.Session()
        self.timeout = timeout

    def get_price_dto(self) -> PriceDTO:
        pass