from datetime import datetime
from scraper.scraper import *
from data_storage import enums as db_enums
from data_storage import utils as db_utils


class Adorama(CloudBaseScraper):
    def __init__(self):
        super().__init__(db_enums.SuperCatalog.Adorama.value)
        self.brands_selector = "brand-list"

    def process_brand_page(self):
        soup = self.get_page_source_as_soup()
        brand_rows_element = soup.find_all("nav", {"class": self.brands_selector})
        for brand_row_element in brand_rows_element:
            a_tags = brand_row_element.find_all("a")
            self.fetch_brand_a_tags(a_tags)


class BH(CloudBaseScraper):
    def __init__(self):
        super().__init__(db_enums.SuperCatalog.BH.value)
        self.brands_selector = "sbb_listWrapper"

    def process_brand_page(self):
        soup = self.get_page_source_as_soup()
        brand_rows_element = soup.find_all("ul", {"class": self.brands_selector})
        for brand_row_element in brand_rows_element:
            a_tags = brand_row_element.find_all("a")
            self.fetch_brand_a_tags(a_tags)


class CCI(SeleniumBaseScraper):
    def __init__(self):
        super().__init__(db_enums.SuperCatalog.CCI.value)
        self.brands_selector = "brand"

    def process_brand_page(self):
        soup = self.get_page_source_as_soup()
        a_tags = soup.find_all("a", {"class": self.brands_selector})
        for a_tag in a_tags:
            try:
                name = a_tag.text
                url = self.get_domain_url() + a_tag["href"]
                self.add_brand(name, url)
            except:
                pass


class CDW(SeleniumBaseScraper):
    def __init__(self):
        super().__init__(db_enums.SuperCatalog.CDW.value)
        self.brands_selector = "cdwgridlayout parbase section"

    def process_brand_page(self):
        soup = self.get_page_source_as_soup()
        row_element = soup.select_one("#brand0-9")
        while 1:
            if row_element.has_attr("class") and self.brands_selector in " ".join(
                row_element.get("class")
            ):
                break
            row_element = row_element.parent

        i = 1
        while 1:
            i += 1
            row_element = row_element.find_next_sibling("div")
            if not row_element:
                break

            if i % 2 == 0:
                a_tags = row_element.find_all("a")
                for a_tag in a_tags:
                    try:
                        name = a_tag.text
                        url = self.get_domain_url() + a_tag["href"]
                        self.add_brand(name, url)
                    except:
                        pass


class EmpirePro(SeleniumBaseScraper):
    def __init__(self):
        super().__init__(db_enums.SuperCatalog.EmpirePro.value)
        self.brands_selector = "items-grid"

    def process_brand_page(self):
        soup = self.get_page_source_as_soup()
        brand_rows_element = soup.find_all("div", {"class": self.brands_selector})
        for brand_row_element in brand_rows_element:
            a_tags = brand_row_element.find_all("a")
            for a_tag in a_tags:
                try:
                    name = a_tag.find("img")["alt"]
                    url = self.get_domain_url() + a_tag["href"]
                    self.add_brand(name, url)
                except:
                    pass


class FullCompass(SeleniumBaseScraper):
    def __init__(self):
        super().__init__(db_enums.SuperCatalog.FullCompass.value)
        self.brands_selector = "showAllBrandGroup"

    def process_brand_page(self):
        soup = self.get_page_source_as_soup()
        brand_rows_element = soup.find_all("div", {"class": self.brands_selector})
        for brand_row_element in brand_rows_element:
            a_tags = brand_row_element.find_all("a")
            self.fetch_brand_a_tags(a_tags)


class OneSourceVideo(SeleniumBaseScraper):
    def __init__(self):
        super().__init__(db_enums.SuperCatalog.OneSourceVideo.value)
        self.brands_selector = "group-row"

    def process_brand_page(self):
        soup = self.get_page_source_as_soup()
        brand_rows_element = soup.find_all("div", {"class": self.brands_selector})
        for brand_row_element in brand_rows_element:
            try:
                name = utils.slug_to_name(brand_row_element["class"][-1])
                url = brand_row_element.find("div", {"class": "brand-browse"}).find(
                    "a"
                )["href"]
                self.add_brand(name, url)
            except:
                pass


class StageLightingStore(SeleniumBaseScraper):
    def __init__(self):
        super().__init__(db_enums.SuperCatalog.StageLightingStore.value)
        self.brands_selector = "facets-category-cell-title"

    def process_brand_page(self):
        soup = self.get_page_source_as_soup()
        brand_rows_element = soup.find_all("div", {"class": self.brands_selector})
        for brand_row_element in brand_rows_element:
            a_tag = brand_row_element.find("a")
            try:
                name = a_tag.text
                url = self.get_domain_url() + a_tag["href"]
                self.add_brand(name, url)
            except:
                pass


class SweetWater(SeleniumBaseScraper):
    def __init__(self):
        super().__init__(db_enums.SuperCatalog.SweetWater.value)
        self.brands_selector = "manuList"

    def process_brand_page(self):
        soup = self.get_page_source_as_soup()
        brand_rows_element = soup.find_all("div", {"id": self.brands_selector})
        for brand_row_element in brand_rows_element:
            a_tags = brand_row_element.find_all("a")
            for a_tag in a_tags:
                try:
                    name = a_tag.text
                    url = self.get_domain_url() + a_tag["href"]
                    self.add_brand(name, url)
                except:
                    pass


class TecNec(SeleniumBaseScraper):
    def __init__(self):
        super().__init__(db_enums.SuperCatalog.TecNec.value)

    def process_brand_page(self):
        brands_config = self.super_catalog_config["brands"]
        brand_selector_paths = brands_config["selector_path"]

        a_tags = self.find_elements("xpath", brand_selector_paths["main"])
        for a_tag in a_tags:
            name = a_tag.get_attribute("text")
            url = a_tag.get_attribute("href")
            self.add_brand(name, url)

    def process_item_page(self, link):
        item_config = self.super_catalog_config["item"]
        self.scrape_web_page(link)
        soup = self.get_page_source_as_soup()
        item_selector_paths = item_config["selector_path"]
        main_elem = soup.select_one(item_selector_paths["main"])
        name = main_elem.select_one(item_selector_paths["name"]).text
        url = link

        vendor_sku = soup.select_one(item_selector_paths["vendor_sku"]).text
        vendor_sku = db_utils.clean_text(vendor_sku)

        manufacturer_sku = soup.select_one(item_selector_paths["manufacturer_sku"]).text
        manufacturer_sku = db_utils.clean_text(manufacturer_sku)
        manufacturer_sku = db_utils.clean_manufacturer_sku(manufacturer_sku)

        currency_code = self.super_catalog_config["currency_code"]
        prices = []
        for price_path in item_selector_paths["prices"]:
            price_elems = soup.select(price_path)

            for price_elem in price_elems:
                try:
                    price_type, amount = price_elem.text.split(":")[:2]

                    price_type = db_utils.clean_text(price_type)
                    price_type = db_utils.clean_price(price_type)

                    amount = db_utils.clean_text(amount)
                    amount = db_utils.clean_amount(amount)

                    prices.append(
                        {
                            "isHistoric": False,
                            "firstSeen": datetime.utcnow(),
                            "lastSeen": datetime.utcnow(),
                            "amount": amount,
                            "currencyCode": currency_code,
                            "priceType": price_type,
                        }
                    )
                except Exception as e:
                    print(e)

        self.item_counter += 1
        item = {
            "itemName": utils.clean_text(name),
            "itemUrl": url,
            "manufacturerSku": manufacturer_sku,
            "vendorSku": vendor_sku,
            "prices": prices,
        }
        self.items.append(item)

    def process_listing_page(self):
        try:
            items_config = self.super_catalog_config["items"]
            soup = self.get_page_source_as_soup()
            items_selector_paths = items_config["selector_path"]
            items_elements = soup.find_all(
                items_selector_paths["main"][0], items_selector_paths["main"][1]
            )
            for item_element in items_elements:
                try:
                    amount = (item_element.select_one(".final_price").text,)
                    prices = [
                        {
                            "isHistoric": False,
                            "firstSeen": datetime.utcnow(),
                            "lastSeen": datetime.utcnow(),
                            "amount": db_utils.clean_amount(amount[0]),
                            "currencyCode": self.super_catalog_config["currency_code"],
                            "priceType": "Dealer",
                        }
                    ]
                    item = {
                        "itemName": utils.clean_text(
                            item_element.select_one("h2 > a").text
                        ),
                        "itemUrl": item_element.select_one("h2 > a")["href"],
                        "status": None,
                        "vendorSku": item_element.select_one(
                            ".cat_item_part_number > a"
                        ).text,
                        "manufacturerSku": None,
                        "prices": prices,
                    }
                except Exception as e:
                    print(e)
                self.items.append(item)

        except Exception as e:
            print(e)

    def process_item_pages(self):
        try:
            items_config = self.super_catalog_config["items"]
            soup = self.get_page_source_as_soup()
            items_selector_paths = items_config["selector_path"]
            items_elements = soup.find_all(
                items_selector_paths["main"][0], items_selector_paths["main"][1]
            )
            for item_element in items_elements:
                link = item_element.select_one("h2 > a")["href"]
                self.process_item_page(link)
                # if len(self.items) > 3:
                #     break
        except Exception as e:
            print(e)
