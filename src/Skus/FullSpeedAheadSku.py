from enum import Enum
from .BaseSku import BaseSku

_ENERGY_HANDLEBAR_38CM_VARIANT_ID = 32882646679629
_OMEGA_STEM_90MM_VARIANT_ID = 46394515456190
_ENERGY_STEM_90MM_VARIANT_ID = 46395174158526
_HEADSET_SPACER_KIT_VARIANT_ID = 32835022389325


class FullSpeedAheadSku(BaseSku):
    """A single sellable product from Full Speed Ahead."""
    def __init__(self, product_slug: str, variant_id: int) -> None:
            self.product_slug = product_slug
            self.variant_id = variant_id

    @property
    def url(self) -> str:
        return f"https://www.fsaproshop.com/products/{self.product_slug}.json"

    @property
    def product_name(self) -> str:
        return self.product_slug.replace('-', ' ')


class FullSpeedAheadSkus(FullSpeedAheadSku, Enum):
    ENERGY_SUPER_COMPACT_HANDLEBAR = ("energy-super-compact-handlebar", _ENERGY_HANDLEBAR_38CM_VARIANT_ID)
    OMEGA_STEM = ("omega-stem", _OMEGA_STEM_90MM_VARIANT_ID)
    ENERGY_STEM = ("energy-stem", _ENERGY_STEM_90MM_VARIANT_ID)
    HEADSET_SPACER_KIT = ("headset-spacer-kit-w-fsa-logo-assorted-sizes-1",
                          _HEADSET_SPACER_KIT_VARIANT_ID)
