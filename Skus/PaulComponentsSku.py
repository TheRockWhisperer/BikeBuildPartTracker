from enum import Enum

class PaulCompSku:
    """A single sellable variant on paulcomp.com."""
    def __init__(self, product_slug: str, variant_id: int):
        self.product_type = "bar_end_plugs"
        self.product_brand = "paul_components"
        self.product_slug = product_slug
        self.variant_id = variant_id

    @property
    def url(self) -> str:
        return f"https://www.paulcomp.com/shop/accessories-apparel/accessories/{self.product_slug}/"

    @property
    def product_name(self) -> str:
        return self.product_slug.replace("-", " ")


class PaulCompProductSkus(PaulCompSku, Enum):
    BAR_END_PLUGS_BLACK = ("bar-end-plugs", 61763)
    BAR_END_PLUGS_SILVER = ("bar-end-plugs", 61764)
    BAR_END_PLUGS_POLISHED = ("bar-end-plugs", 62532)
