from enum import Enum
from .BaseSku import BaseSku


class VelocitWheelsSku(BaseSku):
    """A single sellable variant on velocityusa.com."""
    def __init__(self, product_slug: str, variant_reference_name: str, variant_id: int) -> None:
        self.product_type = "wheelset"
        self.product_brand = "velocity"
        self.product_slug = product_slug
        self.variant_id = variant_id
        self.variant_reference_name = variant_reference_name

    @property
    def url(self) -> str:
        return (
            f"https://velocityusa.com/collections/touring/products/"
            f"{self.product_slug}.json"
        )


class VelocityProductSkus(VelocitWheelsSku, Enum):
    DRYAD_WHEELSET = ("dyad-standard-disc-wheelset", "650b_quick_release", 44508523790415)
