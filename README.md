# Scraper

## Supported Vendors


- TecNec


## Sample Hits

### Super Catalog

```sh
https://alta-scraper-dot-alta-etl.uc.r.appspot.com/scrap-catalog-data?catalogUrl=https://www.tecnec.com/shop-by-brand&catalogType=SuperCatalog&firestoreTaskId=Vendors/zzzzzzzzzzzzzzzzzzzx/Tasks/WdUVA421jarNbrE6MSiy&vendorName=TecNec
```

### Catalog

```sh
https://alta-scraper-dot-alta-etl.uc.r.appspot.com/scrap-catalog-data?catalogUrl=https://www.tecnec.com/brand/ily-enterprise-inc&catalogType=Catalog&firestoreTaskId=Vendors/zzzzzzzzzzzzzzzzzzzx/Catalogs/4e2176e26bf548ad8a53b2804fbc9816/Tasks/9i08RxvViQBQ8ZnBBbB5&vendorName=TecNec
```


## GAE Deployment
Build a docker container
```sh
docker build . --tag alta-scraper
```
```sh
docker image tag alta-scraper  us.gcr.io/alta-etl/alta-scraper
```
Push it on Google Cloud Storage
```sh
docker push us.gcr.io/alta-etl/alta-scraper
```
Deploy app on GAE
```sh
gcloud app deploy --image-url=us.gcr.io/alta-etl/alta-scraper
```
