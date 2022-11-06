from data_storage.data_storage import DataStorage


def populate_vendor():
    name = "Tecnec Distributing"
    data_acquisition_method = "Auto - Web Scrape"
    vendor_type = ["Ecommerce Retailer", "Distributor"]
    vendor_website = "https://www.tecnec.com/"

    data_storage = DataStorage(vendor_website)
    data_storage.save_vendor(name, data_acquisition_method, vendor_type)


def main():
    populate_vendor()


if __name__ == "__main__":
    main()
