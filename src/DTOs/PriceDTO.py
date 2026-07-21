from dataclasses import dataclass
from datetime import date

@dataclass
class PriceDTO:
    product_id: str
    name: str
    date: date
    msrp_price: float
    sale_price: float
    currency: str = "USD"