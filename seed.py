from supabase import create_client, Client
import os
from dotenv import load_dotenv

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

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SERVICE_KEY")

supabase: Client = create_client(url, key)

bicycle_rows = [
    {
        "name": "endurance_road",
        "description": "My Sunday sports car of bikes. Used for endurance training and leisurely road rides."
    },
    {
        "name": "commuter_road",
        "description": "My bike for getting around town without needing to haul anything and social rides. It is speedy but not high-end that I'd worry about hitting a pothole."
    },
    {
        "name": "commuter_touring",
        "description": "My bike for hauling things, night rides, rain, and touring. The workhorse."
    }
]

product_sku_catalogs = [
    CondorProductSkus,
    FullSpeedAheadSkus,
    WhiteIndustriesProductSkus,
    PaulCompProductSkus,
    RitcheyLogicSkus,
    SelleItaliaProductSkus,
    SupacazSkus,
    VittoriaProductSkus,
    MerlinCyclesSkus,
    ChrisKingProductSkus,
    PanaracerProductSkus,
    PDWProductSkus,
    VelocityProductSkus
]

if __name__ == "__main__":
    # Bicycle Table Population
    supabase.table("bicycles").insert(bicycle_rows).execute()
    
    # Product Table Population
    product_rows = []
    for sku_catalog in product_sku_catalogs:
        for product_sku in sku_catalog:
            row = {
                "product_type": product_sku.product_type,
                "product_name_id": product_sku.product_slug,
                "product_brand": product_sku.product_brand,
                "variant": product_sku.variant_id,
                "website": product_sku.url,
            }
            product_rows.append(row)
    supabase.table("products").insert(product_rows).execute()