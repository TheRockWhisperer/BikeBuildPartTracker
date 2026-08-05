from enum import Enum
from .BaseSku import BaseSku


class CondorSku(BaseSku):
    """A single sellable variant on condorcycles.com."""
    def __init__(self, product_type: str, product_slug: str, variant_id: int) -> None:
        self.product_type = product_type
        self.product_brand = "condor"
        self.product_slug = product_slug
        self.variant_id = variant_id

    @property
    def url(self) -> str:
        return (
            f"https://www.condorcycles.com/en-us/products/"
            f"condor-{self.product_slug}.json"
        )


class CondorProductSkus(CondorSku, Enum):
    BLUE_CONDOR_FRAME = ("frame", "fratello-disc-thru-axle-frameset", 49351522615617)
    RED_CONDOR_FRAME  = ("frame", "fratello-disc-thru-axle-frameset", 55310658929024)
    TPU_TUBE_BUNDLE   = ("tube", "tpu-inner-tube-bundle", 56942405157248)
    TPU_REPAIR_KIT    = ("tube", "tpu-inner-tube-patch-repair-kit", 56434152472960)
