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
from Skus.ChrisKingSku import ChrisKingProductSkus
from Skus.PanaracerSku import PanaracerProductSkus
from Skus.PDWSku import PDWProductSkus
from Skus.VelocityWheelsSku import VelocityProductSkus
from Skus.ReserveSku import ReserveProductSkus

from supabase import Client, create_client
import os
from datetime import datetime

RUN_LOCAL = False
if RUN_LOCAL:
    from dotenv import load_dotenv
    load_dotenv()


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# (client, sku, label) — label is just for logging
SCRAPE_JOBS = [
    (ShopifyWebClient(), CondorProductSkus.BLUE_CONDOR_FRAME, "Condor"),
    (ShopifyWebClient(), CondorProductSkus.RED_CONDOR_FRAME, "Condor"),
    (ShopifyWebClient(), CondorProductSkus.TPU_REPAIR_KIT, "Condor"),
    (ShopifyWebClient(), CondorProductSkus.TPU_TUBE_BUNDLE, "Condor"),
    (ShopifyWebClient(), ChrisKingProductSkus.RESERVE_KING_FRAMESET, "Chris King"),
    (WhiteIndustriesWebClient(), WhiteIndustriesProductSkus.CLD_ALUMINUM_700C_ROAD_WHEELS, "White Industries"),
    (ShopifyWebClient(), VittoriaProductSkus.CORSA_PRO_TUBE_TYPE_32C_PARA, "Vittoria"),
    (ShopifyWebClient(), VittoriaProductSkus.RUBINO_TUBE_TYPE_34C_TAN_, "Vittoria"),
    (ShopifyWebClient(), FullSpeedAheadSkus.ENERGY_STEM, "Full Speed Ahead"),
    (ShopifyWebClient(), FullSpeedAheadSkus.ENERGY_SUPER_COMPACT_HANDLEBAR, "Full Speed Ahead"),
    (ShopifyWebClient(), FullSpeedAheadSkus.HEADSET_SPACER_KIT, "Full Speed Ahead"),
    (ShopifyWebClient(), FullSpeedAheadSkus.OMEGA_STEM, "Full Speed Ahead"),
    (ShopifyWebClient(), FullSpeedAheadSkus.SMR_ACR_STEM, "Full Speed Ahead"),
    (ShopifyWebClient(), PanaracerProductSkus.GRAVEL_KINGS, "Panaracer"),
    (SupacazWebClient(), SupacazSkus.SSK_STAR_FADE_RED, "Supacaz"),
    (MerlinCyclesWebClient(), MerlinCyclesSkus.SHIMANO_105_MECHANICAL_GROUPSET, "Merlin Cycles"),
    (MerlinCyclesWebClient(), MerlinCyclesSkus.SHIMANO_105_DI2_GROUPSET, "Merlin Cycles"),
    (MerlinCyclesWebClient(), MerlinCyclesSkus.SHIMANO_ULTEGRA_DI2_GROUPSET, "Merlin Cycles"),
    (RitcheyWebClient(), RitcheyLogicSkus.COMP_ZERO_SEATPOST, "Ritchey Logic"),
    (SelleItaliaWebClient(), SelleItaliaProductSkus.SLR_BOOST_ENDURANCE_L3_BLACK, "Selle Italia"),
    (PaulCompWebClient(), PaulCompProductSkus.BAR_END_PLUGS_BLACK, "Paul Components"),
    (PaulCompWebClient(), PaulCompProductSkus.BAR_END_PLUGS_POLISHED, "Paul Components"),
    (PaulCompWebClient(), PaulCompProductSkus.BAR_END_PLUGS_SILVER, "Paul Components"),
    (ShopifyWebClient(), PDWProductSkus.FULL_METAL_FENDERS, "PDW"),
    (ShopifyWebClient(), PDWProductSkus.TACO_BAR_TAPE, "PDW"),
    (ShopifyWebClient(), VelocityProductSkus.DRYAD_WHEELSET, "Velocity Wheels"),
    (ShopifyWebClient(), ReserveProductSkus.RESERVE_34_37_ENDURANCE, "Reserve Wheels"),
    (ShopifyWebClient(), ReserveProductSkus.RESERVE_42_49_ENDURANCE, "Reserve Wheels"),
]


def run_scrape() -> dict:
    dto_list: list[PriceDTO] = []
    errors: list[dict] = []

    for client, sku, label in SCRAPE_JOBS:
        try:
            dto = client.fetch_price_dto(sku)
            price_model: dict = {
                "time": dto.date.isoformat(),
                "product_type": sku.product_type,
                "product_brand": sku.product_brand,
                "product_name": dto.product_id,
                "variant": sku.variant_reference_name,
                "msrp_price": dto.msrp_price,
                "sale_price": dto.sale_price
            }
            dto_list.append(price_model)
            logger.info(f"Fetched {label}: {dto}")
        except Exception as e:
            logger.error(f"Failed to fetch {label}: {e}")
            errors.append({"source": label, "error": str(e)})

    # Adding the Siena frameset, they don't offer sales
    dto_list.append(
        {
            "time": datetime.now().isoformat(),
            "product_type": "frame",
            "product_brand": "officina_battaglin",
            "product_name": "siena-frameset",
            "variant": "regular_paint_finish",
            "msrp_price": 2459,
            "sale_price": None
        }
    )

    url = "https://mutrifzqzvsxxhgcyxrl.supabase.co"
    key = "sb_publishable_52B0sXyVjxvrPAw7OMkzoQ_ANruGm9E"
    
    url = os.environ["SUPABASE_URL"]
    key = os.environ["SUPABASE_SERVICE_KEY"]
    supabase: Client = create_client(url, key)

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
