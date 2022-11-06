import process
from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def hello():
    msg = """
    Welcome <br><br>
    Sample Super Catalog hit <br>
    https://alta-scraper-dot-alta-etl.uc.r.appspot.com/scrap-catalog-data?catalogUrl=https://www.tecnec.com/shop-by-brand&catalogType=SuperCatalog&firestoreTaskId=Vendors/zzzzzzzzzzzzzzzzzzzx/Tasks/WdUVA421jarNbrE6MSiy&vendorName=TecNec
    <br><br>
    Sample Catalog hit <br>
    https://alta-scraper-dot-alta-etl.uc.r.appspot.com/scrap-catalog-data?catalogUrl=https://www.tecnec.com/brand/ily-enterprise-inc&catalogType=Catalog&firestoreTaskId=Vendors/zzzzzzzzzzzzzzzzzzzx/Catalogs/4e2176e26bf548ad8a53b2804fbc9816/Tasks/9i08RxvViQBQ8ZnBBbB5&vendorName=TecNec
    <br><br>
    Supported CatalogTypes = ['SuperCatalog', 'Catalog']<br>
    Supported Vendors = ['TecNec']<br>

    """
    return msg


@app.route("/scrap-catalog-data")
def scrap_catalog_data():
    is_success = 1
    error_details = ""
    try:
        catalog_url = request.args.get("catalogUrl")
        catalog_type = request.args.get("catalogType")
        firestore_task_id = request.args.get("firestoreTaskId")
        vendor_name = request.args.get("vendorName")

        if not catalog_url:
            is_success = 0
            error_details += (
                "Insufficient Data Provided. Details: No 'catalogUrl' provided."
            )

        if not catalog_type:
            is_success = 0
            error_details += (
                "Insufficient Data Provided. Details: No 'catalogType' provided."
            )

        if not firestore_task_id:
            is_success = 0
            error_details += (
                "Insufficient Data Provided. Details: No 'firestoreTaskId' provided."
            )

        if not vendor_name:
            is_success = 0
            error_details += (
                "Insufficient Data Provided. Details: No 'vendorName' provided."
            )

        if is_success:
            data = {
                "catalog_url": catalog_url,
                "catalog_type": catalog_type,
                "firestore_task_id": firestore_task_id,
                "vendor_name": vendor_name,
            }
            is_success, err_details = process.main(data)
            error_details += err_details

    except Exception as e:
        print(e)
        is_success = 0
        error_details = f"Error occurred while processing. Details: {str(e)}"

    return {"is_success": is_success, "error_details": error_details}


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
