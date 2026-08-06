from enum import Enum
from .BaseSku import BaseSku


class ReserveSku(BaseSku):
    """A single sellable variant on reservewheels.com."""
    def __init__(self, product_slug: str, variant_reference_name: str, variant_id: int) -> None:
        self.product_type = "wheelset"
        self.product_brand = "reserve"
        self.product_slug = product_slug
        self.variant_id = variant_id
        self.variant_reference_name = variant_reference_name

    @property
    def url(self) -> str:
        return (
            f"https://reservewheels.com/products/{self.product_slug}.json"
        )


class ReserveProductSkus(ReserveSku, Enum):
    RESERVE_42_49_ENDURANCE = ("reserve-42-49", "endurance_dt350_hubs", 44140096815285)
    RESERVE_34_37_ENDURANCE  = ("reserve-34-37-turbulent-aero", "climbing_dt350_hubs", 44327449460917)
