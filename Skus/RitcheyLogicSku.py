from Skus.BaseSku import BaseSku
from enum import Enum

class RitcheySku(BaseSku):
    """A single sellable product variant on ritcheylogic.com.

    product_path is the full URL path segment (varies by category:
    e.g. 'bike/frames/p-29er-frame' vs 'product/wcs-carbon-mountain-adventure-fork'),
    since Ritchey doesn't use one consistent prefix across product types.
    """
    def __init__(self, product_slug: str, variant_id: int) -> None:
            self.product_type = "seatpost"
            self.product_brand = "ritchey_logic"
            self.product_slug = product_slug
            self.variant_id = variant_id

    @property
    def url(self) -> str:
        return f"https://ritcheylogic.com/{self.product_slug}?sku={str(self.variant_id)}"

    @property
    def sku(self) -> str:
         return str(self.variant_id)

    @property
    def product_name(self) -> str:
        return self.product_slug.rsplit("/", 1)[-1].replace('-', ' ')


class RitcheyLogicSkus(RitcheySku, Enum):
    COMP_ZERO_SEATPOST = ('bike/seatposts/comp-zero-seatpost', 41035317055)