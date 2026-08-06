from enum import Enum
from .BaseSku import BaseSku


class ChrisKingSku(BaseSku):
    """A single sellable variant on condorcycles.com."""
    def __init__(self, product_slug: str, variant_reference_name: str, variant_id: int) -> None:
        self.product_type = "wheelset"
        self.product_brand = "chris_king_and_reserve"
        self.product_slug = product_slug
        self.variant_id = variant_id
        self.variant_reference_name = variant_reference_name

    @property
    def url(self) -> str:
        return (
            f"https://chrisking.com/collections/reserve/products/"
            f"{self.product_slug}.json"
        )


class ChrisKingProductSkus(ChrisKingSku, Enum):
    RESERVE_KING_FRAMESET = ("reserve-42-49ta-r45d", "chris_king_hubs", 42753926660214)