from enum import Enum
from .BaseSku import BaseSku


class CaneCreekSku(BaseSku):
    """A single sellable variant on condorcycles.com."""
    def __init__(self, product_type: str, product_slug: str, variant_reference_name: str, variant_id: int) -> None:
        self.product_type = product_type
        self.product_brand = "cane_creek"
        self.product_slug = product_slug
        self.variant_id = variant_id
        self.variant_reference_name = variant_reference_name

    @property
    def url(self) -> str:
        return (
            f"https://www.canecreek.com/products/{self.product_slug}.json"
        )


class CaneCreekProductSkus(CaneCreekSku, Enum):
    HCR_HEADSET = ("headset", "hcr-headset", "hcr_headset_is", 43980351340623)
    HCR_STEM = ("stem", "hcr-stem", "hcr_stem_90mm", 43690058907727)
