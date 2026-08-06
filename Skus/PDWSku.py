from enum import Enum
from .BaseSku import BaseSku


class PDWSku(BaseSku):
    """A single sellable variant on ridepdw.com."""
    def __init__(self, product_type: str, product_slug: str, variant_reference_name: str, variant_id: int) -> None:
        self.product_type = product_type
        self.product_brand = "pdw"
        self.product_slug = product_slug
        self.variant_id = variant_id
        self.variant_reference_name = variant_reference_name

    @property
    def url(self) -> str:
        return (
            f"https://ridepdw.com/collections/fenders/products/"
            f"{self.product_slug}.json"
        )

class PDWProductSkus(PDWSku, Enum):
    FULL_METAL_FENDERS = ("fenders", "full-metal-fenders-city-size", "37c_full_metal", 14871301488697)
    TACO_BAR_TAPE  = ("bar_tape", "pdw-wraps-with-silicone-grip", "tacos", 36879248949416)
