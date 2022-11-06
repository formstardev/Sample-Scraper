from datetime import datetime
from scraper.super_catalogs import *
from data_storage import enums
from data_storage import utils as db_utils
from data_storage.data_storage import DataStorage

super_catalog_urls = {
    enums.SuperCatalog.Adorama.value: "https://www.adorama.com/brands",
    enums.SuperCatalog.BH.value: "https://www.bhphotovideo.com/c/browse/Shop-by-Brand/ci/9028/N/4291093803",
    enums.SuperCatalog.CCI.value: "https://www.ccisolutions.com/StoreFront/category/shop-by-brand",
    enums.SuperCatalog.CDW.value: "https://www.cdw.com/content/cdw/en/brand.html",
    enums.SuperCatalog.EmpirePro.value: "https://www.empirepro.com/catalog/category/view/s/pro-brands/id/8/",
    enums.SuperCatalog.FullCompass.value: "https://www.fullcompass.com/brands_show_all.php",
    enums.SuperCatalog.OneSourceVideo.value: "https://1sourcevideo.com/shop/index.php/brands",
    enums.SuperCatalog.StageLightingStore.value: "https://www.stagelightingstore.com/shop-by-brand",
    enums.SuperCatalog.SweetWater.value: "https://www.sweetwater.com/store/manufacturer/all",
    enums.SuperCatalog.TecNec.value: "https://www.tecnec.com/shop-by-brand",
}


def scraper(data):
    super_catalog_name = data.get("super_catalog")
    class_name = enums.SuperCatalog(super_catalog_name).name
    constructor = globals()[class_name]
    scraper_obj = constructor()

    scraper_obj.process()
    vendor_info = settings.SUPER_CATALOG_TEMPLATES[enums.SuperCatalog.TecNec.value][
        "vendor_info"
    ]
    data_storage = DataStorage(vendor_info["website"])
    data_storage.set_items(scraper_obj.items)
    data_storage.save_items()
    scraper_obj.end_process()


def process_super_catalog(data={}):
    vendor_info = settings.SUPER_CATALOG_TEMPLATES[enums.SuperCatalog.TecNec.value][
        "vendor_info"
    ]
    data_storage = DataStorage(vendor_info["website"])
    data_storage.update_actor_time(data.get("firestore_task_id"), "actorStartTime")

    vendor_name = data.get("vendor_name")
    catalog_url = data.get("catalog_url")

    class_name = enums.SuperCatalog(vendor_name).name
    constructor = globals()[class_name]
    scraper_obj = constructor()

    scraper_obj.process_brands(catalog_url)

    data_storage.set_catalogs(scraper_obj.brands)

    data_storage.save_catalogs()
    data_storage.update_actor_time(data.get("firestore_task_id"), "actorEndTime")


def process_catalog(data={}):
    vendor_info = settings.SUPER_CATALOG_TEMPLATES[enums.SuperCatalog.TecNec.value][
        "vendor_info"
    ]
    data_storage = DataStorage(vendor_info["website"])
    data_storage.update_actor_time(data.get("firestore_task_id"), "actorStartTime")

    vendor_name = data.get("vendor_name")
    catalog_url = data.get("catalog_url")
    class_name = enums.SuperCatalog(vendor_name).name
    constructor = globals()[class_name]
    scraper_obj = constructor()

    scraper_obj.process_listing(catalog_url)

    data_storage.set_items(scraper_obj.items)
    data_storage.save_items(catalog_url)

    data_storage.update_actor_time(data.get("firestore_task_id"), "actorEndTime")


def main(data={}):
    is_success = 1
    error_details = ""
    catalog_type = data["catalog_type"]
    if catalog_type == db_enums.CatalogType.SuperCatalog.value:
        process_super_catalog(data)
    elif catalog_type == db_enums.CatalogType.Catalog.value:
        process_catalog(data)

    return is_success, error_details


def rough():
    from bs4 import BeautifulSoup

    ### FOR PRICES
    html_string = """
    <div id="product-pricing"><p class="product-variable">Weight: <span id="Variant0Weight">0.25</span></p><p class="product-listprice"><span id="Variant0ListTitle">List Price:</span> <span id="Variant0ListValue">$299.00</span></p><div id="CustomMessageContainer" style="display:none"><div class="clear">&nbsp;</div><p class="product-availability">Availability: <span id="Variant0Stock" class="instock">3 In Stock</span><span class="instock availability_icon" title="Item is Available for immediate shipping from our warehouse."><img src="https://www.tecnec.com/assets/images/AvbInfo.png" class="infoimg" alt="Availability Information" /></span></p><p class="productmobile-availability">Item is Available for immediate shipping from our warehouse.</p><p class="product-note"></p><p  class="product-warningmsg">California Residents:<br/><img src="https://www.tecnec.com/assets/images/8pt-triangle.png" class="triimg" alt="" /><span><span class="warn">WARNING</span>: Cancer and Reproductive Harm<br/><a href="http://www.p65warnings.ca.gov/" target="_blank">www.P65Warnings.ca.gov</a></span></p></div><div id="ProductDataContainerPart1" ><p class="product-listprice"><span id="Variant0Price1Title">Dealer Price:</span> <span id="Variant0Price1Value" style="text-decoration:line-through;" >$279.00</span></p><p class="product-ourprice"><span id="Variant0Price2Title">Special Price:</span> <span id="Variant0Price2Value" style="color:#cc0000;">$39.00</span></p><div class="product-actions"><div class="cart-item-qty">Quantity:<input type="text" class="qty_input" name="Quantity" id="Quantity" value="1" maxlength="4" onkeypress="javascript:return isNumber(event)" onblur="javascript:return isNumber(event)" /></div><div class="add-to-cart"><input type="button" id="AddToCart" value="Add To Cart" class="btn btn-primary btn-lg gtm_tn_addtocart" /><br /><a id="AddToWishlist" class="wish-list gtm_tn_addtowishlist" href="javascript:AddToWishlist('WI-SE-32','')"> Add to Wish List</a><a id="AddToQuote" class="add_to_link" style="display:none" href="#"> + Add to Quote</a></div></div><div id="ProductDataContainerPart2" ><p class="product-availability">Availability: <span id="Variant0Stock" class="instock stockstatus">3 In Stock</span><span class="instock availability_icon" title="Item is Available for immediate shipping from our warehouse."><img src="https://www.tecnec.com/assets/images/AvbInfo.png" class="infoimg" alt="Availability Information" /></span></p><p class="productmobile-availability">Item is Available for immediate shipping from our warehouse.</p><p class="product-note"></p><p style="display:none" class="product-qty"><span id="Variant0QtyDiscount" class="price_label qty_label"><a class="quantity-pricing" href="javascript:ShowQuantityPricing('WI-SE-32')" rel="nofollow">Quantity Pricing</a></span><div style="display:none" id="QtySummary"></div></p><p  class="product-warningmsg">California Residents:<br/><img src="https://www.tecnec.com/assets/images/8pt-triangle.png" class="triimg" alt="" /><span><span class="warn">WARNING</span>: Cancer and Reproductive Harm<br/><a href="http://www.p65warnings.ca.gov/" target="_blank">www.P65Warnings.ca.gov</a></span></p></div></div></div></div></div>
    """
    soup = BeautifulSoup(html_string)
    prices_path = [".product-listprice", ".product-ourprice"]
    for price_path in prices_path:
        price_elems = soup.select(price_path)

        for price_elem in price_elems:
            price_type, amount = price_elem.text.split(":")[:2]
            price_type = db_utils.clean_text(price_type)
            amount = db_utils.clean_text(amount)
            print(price_type, db_utils.clean_amount(amount))

    ###

    html_string = """
    <p class="product_sku">Item #: <span id="Variant0ItemID">WI-SE-32</span><span id="Variant0VendorId" class="hidden-xs">&nbsp; • &nbsp; MFG #: WI-SE-32</span><span id="Variant0MobVendorId" class="visible-xs">MFG #: WI-SE-32</span></p>
    """
    soup = BeautifulSoup(html_string)
    vendor_sku_path = ".product_sku > span:nth-of-type(1)"
    manufacturer_sku_path = ".product_sku > span:nth-of-type(2)"

    vendor_sku = soup.select_one(vendor_sku_path).text
    vendor_sku = db_utils.clean_text(vendor_sku)

    manufacturer_sku = soup.select_one(manufacturer_sku_path).text
    manufacturer_sku = db_utils.clean_text(manufacturer_sku)
    manufacturer_sku = db_utils.clean_manufacturer_sku(manufacturer_sku)
    print(vendor_sku)
    print(manufacturer_sku)


if __name__ == "__main__":
    data = {
        "catalog_url": "https://www.tecnec.com/shop-by-brand",
        "catalog_type": "SuperCatalog",
        "firestore_task_id": "Vendors/zzzzzzzzzzzzzzzzzzzx/Catalogs/4e2176e26bf548ad8a53b2804fbc9816/Tasks/9i08RxvViQBQ8ZnBBbB5",
        "vendor_name": "TecNec",
    }
    # data = {
    #     "catalog_url": "https://www.tecnec.com/brand/ily-enterprise-inc",
    #     "catalog_type": "Catalog",
    #     "firestore_task_id": "Vendors/zzzzzzzzzzzzzzzzzzzx/Catalogs/4e2176e26bf548ad8a53b2804fbc9816/Tasks/9i08RxvViQBQ8ZnBBbB5",
    #     "vendor_name": "TecNec"
    # }
    main(data)
    vendor_info = settings.SUPER_CATALOG_TEMPLATES[enums.SuperCatalog.TecNec.value]["vendor_info"]
    data_storage = DataStorage(vendor_info["website"])
    data_storage.update_actor_time(data.get("firestore_task_id"), "actorStartTime")

    rough()
