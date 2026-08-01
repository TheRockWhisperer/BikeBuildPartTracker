from enum import Enum
from .BaseSku import BaseSku


class CondorSku(BaseSku):
    """A single sellable variant on condorcycles.com."""
    def __init__(self, product_slug: str, variant_id: int) -> None:
        self.product_slug = product_slug
        self.variant_id = variant_id

    @property
    def url(self) -> str:
        return (
            f"https://www.condorcycles.com/en-us/products/"
            f"condor-{self.product_slug}.json"
        )

    @property
    def product_name(self) -> str:
        return self.product_slug.replace('-', ' ')


class CondorProductSkus(CondorSku, Enum):
    BLUE_CONDOR_FRAME = ("fratello-disc-thru-axle-frameset", 49351522615617)
    RED_CONDOR_FRAME  = ("fratello-disc-thru-axle-frameset", 55310658929024)
    TPU_TUBE_BUNDLE   = ("tpu-inner-tube-bundle", 56942405157248)
    TPU_REPAIR_KIT    = ("tpu-inner-tube-patch-repair-kit", 56434152472960)