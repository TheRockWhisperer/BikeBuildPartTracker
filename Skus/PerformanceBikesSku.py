from enum import Enum
from .BaseSku import BaseSku


class PerformanceBikeProductSku():
    """A single sellable product from Performance Bicycle.

    Performance Bicycle URLs look like:
        https://www.performancebike.com/{product_slug}/p{product_id}
    and, for products with a variant selector (e.g. crankset arm length,
    cassette range), a specific variant is selected via a `v=` query param:
        https://www.performancebike.com/{product_slug}/p{product_id}?v={variant_id}

    variant_id is optional — omit it (or pass None) for single-variant
    products. If a product page has a `ul.variants` block and variant_id
    is left out, the URL will resolve to whichever variant the site
    defaults to, not necessarily the one you want.
    """
    def __init__(
        self,
        product_slug: str,
        product_id: int,
        variant_reference_name: str = "165mm-42t",
        variant_id: int = None,
        product_type: str = "groupset",
        product_brand: str = "sram",
    ):
        self.product_type = product_type
        self.product_brand = product_brand
        self.product_slug = product_slug
        self.product_id = product_id
        self.variant_reference_name = variant_reference_name or "165mm-42t"
        self.variant_id = variant_id

    @property
    def url(self) -> str:
        base_url = f"https://www.performancebike.com/{self.product_slug}/p{self.product_id}"
        if self.variant_id is not None:
            return f"{base_url}?v={self.variant_id}"
        return base_url

    @property
    def product_name(self) -> str:
        return self.product_slug.replace('-', ' ')


class PerformanceBikeSkus(PerformanceBikeProductSku, Enum):
    SRAM_FORCE_XPLR_AXS_GRAVEL_GROUPSET = (
        "sram-force-xplr-axs-gravel-groupset-1-x-13-speed-sramforce-e1grp2-bdl",
        1644909,
    )
    SRAM_RIVAL_1_XPLR_CRANKSET_165MM = (
        "sram-rival-1-xplr-crankset-black-1-x-12-13-speed-dub-wide-165mm-42t-00.6118.742.001",
        1645178,
        "165mm-42t",
        1640045,
    )


class PerformanceBikeBundleSku():
    """A logical purchase made up of multiple separate product pages whose
    prices need to be summed — e.g. a "groupset" that Performance Bicycle
    actually sells as two separate listings (the shifter/derailleur/cassette
    kit, plus the crankset sold on its own page).

    `components` is a tuple of PerformanceBikeProductSku (or Enum members
    that mix it in). PerformanceBikeWebClient fetches each component's page
    independently and sums the results — see fetch_price_dto.
    """
    def __init__(self, bundle_slug: str, components: tuple):
        self.product_type = "groupset"
        self.product_brand = "sram"
        self.variant_reference_name = "165mm-42t"
        self.product_slug = bundle_slug
        self.components = components
        self.url = "https://www.performancebike.com/sram-rival-axs-xplr-gravel-groupset-black-1-x-13-speed-1046t-sramrival-e1grp2-bdl/p1644912"

    @property
    def product_name(self) -> str:
        return self.product_slug.replace('-', ' ')


class PerformanceBikeBundles(PerformanceBikeBundleSku, Enum):
    # CAVEAT: the crankset here (SRAM_RIVAL_1_XPLR_CRANKSET_165MM) is a
    # different SRAM tier than the groupset (Force). A real Force build
    # would pair with a Force crankset SKU instead — this bundle uses the
    # only crankset SKU defined so far, per the request to always use the
    # 165mm crankset. Swap in a matching-tier crankset SKU if that mismatch
    # wasn't intentional.
    SRAM_FORCE_XPLR_COMPLETE_GROUPSET = (
        "sram-force-xplr-complete-groupset-165mm-crank",
        (
            PerformanceBikeSkus.SRAM_FORCE_XPLR_AXS_GRAVEL_GROUPSET,
            PerformanceBikeSkus.SRAM_RIVAL_1_XPLR_CRANKSET_165MM,
        ),
    )