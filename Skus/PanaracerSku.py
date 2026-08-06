from enum import Enum
from .BaseSku import BaseSku


class PanaracerSku(BaseSku):
    """A single sellable variant on panaracerusa.com."""
    def __init__(self, product_slug: str, variant_id: int) -> None:
        self.product_type = "tire"
        self.product_brand = "panaracer"
        self.product_slug = product_slug
        self.variant_id = variant_id

    @property
    def url(self) -> str:
        return (
            f"https://www.panaracerusa.com/products/{self.product_slug}.json"
        )


class PanaracerProductSkus(PanaracerSku, Enum):
    GRAVEL_KINGS = ("gravelking-ss-2024-folding-gravel-tire", 44612765876459)
