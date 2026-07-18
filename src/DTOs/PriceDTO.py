from dataclasses import dataclass

@dataclass
class PriceDTO:
    product_id: str
    name: str
    price: float
    currency: str = "USD"