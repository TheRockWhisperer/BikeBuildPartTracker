import logging
import sys

from DTOs.PriceDTO import PriceDTO
from Clients.ShopifyWebClient import ShopifyWebClient
from Clients.WhiteIndustriesWebClient import WhiteIndustriesWebClient
from Clients.SupacazWebClient import SupacazWebClient
from Clients.MerlinCycles import MerlinCyclesWebClient
from Clients.RitcheyLogicWebClient import RitcheyWebClient
from Clients.SelleItaliaWebClient import SelleItaliaWebClient
from Clients.PaulComponentsWebClient import PaulCompWebClient

from Skus.CondorSku import CondorProductSkus
from Skus.WhiteIndustriesSku import WhiteIndustriesProductSkus
from Skus.VittoriaSku import VittoriaProductSkus
from Skus.FullSpeedAheadSku import FullSpeedAheadSkus
from Skus.SupacazSku import SupacazSkus
from Skus.MerlinCyclesSku import MerlinCyclesSkus
from Skus.RitcheyLogicSku import RitcheyLogicSkus
from Skus.SelleItaliaSku import SelleItaliaProductSkus
from Skus.PaulComponentsSku import PaulCompProductSkus

from supabase import Client, create_client
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# (client, sku, label) — label is just for logging
SCRAPE_JOBS = [
    (ShopifyWebClient(), CondorProductSkus.BLUE_CONDOR_FRAME, "Condor"),
    (WhiteIndustriesWebClient(), WhiteIndustriesProductSkus.CLD_ALUMINUM_700C_ROAD_WHEELS, "White Industries"),
    (ShopifyWebClient(), VittoriaProductSkus.CORSA_PRO_TUBE_TYPE_32C_PARA, "Vittoria"),
    (ShopifyWebClient(), FullSpeedAheadSkus.ENERGY_STEM, "Full Speed Ahead"),
    (SupacazWebClient(), SupacazSkus.SSK_STAR_FADE_RED, "Supacaz"),
    (MerlinCyclesWebClient(), MerlinCyclesSkus.SHIMANO_105_MECHANICAL_GROUPSET, "Merlin Cycles"),
    (RitcheyWebClient(), RitcheyLogicSkus.COMP_ZERO_SEATPOST, "Ritchey Logic"),
    (SelleItaliaWebClient(), SelleItaliaProductSkus.SLR_BOOST_ENDURANCE_L3_BLACK, "Selle Italia"),
    (PaulCompWebClient(), PaulCompProductSkus.BAR_END_PLUGS_BLACK, "Paul Components"),
]


def run_scrape() -> dict:
    dto_list: list[PriceDTO] = []
    errors: list[dict] = []

    for client, sku, label in SCRAPE_JOBS:
        try:
            dto = client.fetch_price_dto(sku)
            price_model: dict = {
                "date": dto.date.isoformat(),
                "product_type": sku.product_type,
                "product_brand": sku.product_brand,
                "product_name": dto.product_id,
                "variant": sku.variant_id,
                "msrp_price": dto.msrp_price,
                "sale_price": dto.sale_price
            }
            dto_list.append(price_model)
            logger.info(f"Fetched {label}: {dto}")
        except Exception as e:
            logger.error(f"Failed to fetch {label}: {e}")
            errors.append({"source": label, "error": str(e)})


    url = os.environ["SUPABASE_URL"]
    key = os.environ["SUPABASE_PUBLISHABLE_KEY"]
    supabase: Client = create_client(url, key)

    supabase.auth.sign_in_with_password({
        "email": os.environ["SCRAPER_EMAIL"],
        "password": os.environ["SCRAPER_PASSWORD"],
    })

    supabase.table("bicycle_product_daily_price").insert(dto_list).execute()

    return {
        "fetched": len(dto_list),
        "failed": len(errors),
        "errors": errors,
    }


if __name__ == "__main__":
    result = run_scrape()

    logger.info(f"Run complete: {result['fetched']} fetched, {result['failed']} failed")

    if result["failed"] > 0:
        for err in result["errors"]:
            logger.error(f"  {err['source']}: {err['error']}")

        # Fail the whole job only if EVERY scraper failed (total outage).
        # Partial failures still exit 0 so the DB insert of successful
        # results isn't treated as a broken workflow — but the errors
        # are logged above so you'll see them in the Actions run.
        if result["fetched"] == 0:
            sys.exit(1)

    sys.exit(0)