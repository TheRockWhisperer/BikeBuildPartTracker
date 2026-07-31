from enum import Enum
from .BaseSku import BaseSku


class VittoriaSku(BaseSku):
    """A single sellable variant on vittoria.com."""
    def __init__(self, product_slug: str, variant_id: int) -> None:
        self.product_slug = product_slug
        self.variant_id = variant_id

    @property
    def url(self) -> str:
        return f"https://vittoria.com/products/{self.product_slug}.json"

    @property
    def product_name(self) -> str:
        return self.product_slug.replace('-', ' ')


class VittoriaProductSkus(VittoriaSku, Enum):
    RUBINO_TUBE_TYPE_34C_TAN_ = ("rubino-tube-type", 50041907413280)
    CORSA_PRO_TUBE_TYPE_32C_PARA  = ("corsa-pro-tube-type", 50041906823456)