from enum import Enum
from Skus.BaseSku import BaseSku


class SupacazProductSku(BaseSku):
    """A single sellable product on supacaz.com."""

    def __init__(self, product_slug: str, variant_reference_name: str) -> None:
        self.product_type = "bar_tape"
        self.product_brand = "supacaz"
        self.product_slug = product_slug
        self.variant_reference_name = variant_reference_name

    @property
    def url(self) -> str:
        return f"https://supacaz.com/product/{self.product_slug}/"

    @property
    def product_name(self) -> str:
        return self.product_slug.replace('-', ' ')


class SupacazSkus(SupacazProductSku, Enum):
    SSK_STAR_FADE_RED = ("super-sticky-kush-star-fade-red", "red")
    SSK_STAR_FADE_WHITE = ("super-sticky-kush-star-fade-white", "white")
    SSK_STAR_FADE_CELESTE = ("super-sticky-kush-star-fade-celeste", "celeste")
    SSK_STAR_FADE_GOLD = ("super-sticky-kush-star-fade-gold", "gold")
    SSK_STAR_FADE_PLATINUM = ("super-sticky-kush-star-fade-platinum", "platinum")
    SSK_STAR_FADE_OIL_SLICK = ("super-sticky-kush-star-fade-oil-slick", "oil_slick")
    SSK_STAR_FADE_NEON_BLUE = ("super-sticky-kush-star-fade-neon-blue", "blue")
    SSK_STAR_FADE_NEON_GREEN = ("super-sticky-kush-star-fade-neon-green", "green")
    SSK_STAR_FADE_NEON_PINK = ("super-sticky-kush-star-fade-neon-pink", "pink")
    SSK_STAR_FADE_NEON_YELLOW = ("super-sticky-kush-star-fade-neon-yellow", "yellow")
