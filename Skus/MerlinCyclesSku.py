from enum import Enum
from .BaseSku import BaseSku


class MerlinCyclesProductSku():
    """A single sellable product from Full Speed Ahead."""
    def __init__(self, product_slug: str, variant_reference_name: str, variant_id: int):
        self.product_type = "groupset"
        self.product_brand = "shimano"
        self.product_slug = product_slug
        self.variant_id = variant_id
        self.variant_reference_name = variant_reference_name

    @property
    def url(self) -> str:
        return f"https://www.merlincycles.com/en-us/{self.product_slug}.html"

    @property
    def product_name(self) -> str:
        return self.product_slug.replace('-', ' ')


class MerlinCyclesSkus(MerlinCyclesProductSku, Enum):
    SHIMANO_105_MECHANICAL_GROUPSET = ("shimano-105-r7120-disc-groupset-12-speed-298406", "mechanical", 7120)
    SHIMANO_105_DI2_GROUPSET = ("shimano-105-r7170-di2-disc-groupset-12-speed-271682", "electronic", 7170)
    SHIMANO_ULTEGRA_DI2_GROUPSET = ("shimano-ultegra-r8170-di2-disc-groupset-12-speed-252965", "electronic", 8100)
