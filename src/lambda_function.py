import logging

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
from Clients.MerlinCycles import MerlinCyclesSkus
from Skus.RitcheyLogicSku import RitcheyLogicSkus
from Skus.SelleItaliaSku import SelleItaliaProductSkus
from Skus.PaulComponentsSku import PaulCompProductSkus

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# (client, sku, label) — label is just for logging
SCRAPE_JOBS = [
    (ShopifyWebClient(), CondorProductSkus.BLUE_CONDOR_FRAME, "Condor"),
    (WhiteIndustriesWebClient(), WhiteIndustriesProductSkus.CLD_ALUMINUM_700C_ROAD_WHEELS, "White Industries"),
    (ShopifyWebClient(), VittoriaProductSkus.CORSA_PRO_TUBE_TYPE_32C_PARA, "Vittoria"),
    (ShopifyWebClient(), FullSpeedAheadSkus.ENERGY_STEM, "Full Speed Ahead"),
    (SupacazWebClient(), SupacazSkus.SSK_STAR_FADE_RED, "Supacaz"),
    (MerlinCyclesWebClient(), MerlinCyclesSkus.SHIMANO_105_MECHANICAL_GROUPSET.value, "Merlin Cycles"),
    (RitcheyWebClient(), RitcheyLogicSkus.COMP_ZERO_SEATPOST, "Ritchey Logic"),
    (SelleItaliaWebClient(), SelleItaliaProductSkus.SLR_BOOST_ENDURANCE_L3_BLACK, "Selle Italia"),
    (PaulCompWebClient(), PaulCompProductSkus.BAR_END_PLUGS_BLACK, "Paul Components"),
]


def handler(event, context):
    dto_list: list[PriceDTO] = []
    errors: list[dict] = []

    for client, sku, label in SCRAPE_JOBS:
        try:
            dto = client.fetch_price_dto(sku)
            dto_list.append(dto)
            logger.info(f"Fetched {label}: {dto}")
        except Exception as e:
            logger.error(f"Failed to fetch {label}: {e}")
            errors.append({"source": label, "error": str(e)})

    # TODO: insert dto_list into your database here
    # insert_records(dto_list)

    return {
        "statusCode": 200 if not errors else 207,  # 207 = partial success
        "fetched": len(dto_list),
        "failed": len(errors),
        "errors": errors,
    }
