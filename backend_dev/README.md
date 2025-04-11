# Backend Dev — API Scripts

## Authors: 
Roan Yeh

## Purpose:
Serves as the endpoint for all API calls

## Necessary installs

Run command 

```
pip install -r requirements.txt  
```

## Profile Page

**Brief Description:**
All API calls are mounted here to run through on endpoint.

**Status** 

In progress...

**Running the API**

uvicorn main:app --reload

**Info**

*Feed*
--------
Swipe right: 

```
curl -X 'GET' \
  'http://localhost:8000/feed/swipe-right/<listing-id>?uid=<uid>'
```

Swipe left:

```
curl -X 'GET' \
  'http://localhost:8000/feed/swipe-left/<listing-id>?uid=<uid>'
```

Swipe down:

```
curl -X 'GET' \
  'http://localhost:8000/feed/swipe-down/<listing-id>?uid=<uid>'
```


*Listings*
--------

Create Listing:
```
curl -X POST "http://127.0.0.1:8000/listings/create-listing" \
  -H "Content-Type: multipart/form-data" \
  -F "title=Banama" \
  -F "long_description=A classic vintage banama in excellent condition." \
  -F "price=27" \
  -F "listing_type=listing" \
  -F "transaction_type=sell" \
  -F "profile_offerer_id=M1TvCTanfGUlLeTYw3NP" \
  -F "tags=home decor" \
  -F "image=@/Users/sneak100/Desktop/HandDown/backend_dev/listing_api/test-images/banama.jpeg"
```

Get Listing:
```
curl http://localhost:8000/listings/get-listing/listing_id
```

Get all Listings:
```
curl http://localhost:8000/listings/get-all-listings
```

Edit Listing Title
```
curl -X POST "http://127.0.0.1:8000/listings/edit-listing-title/fMrg4bMMVspwzbucAR47" \
  -d "new_title=Barama"
```

Edit Listing Description
```
curl -X POST "http://127.0.0.1:8000/listings/edit-listing-description/fMrg4bMMVspwzbucAR47" \
  -d "new_desc=I don't really know what this is but you want it"
```

Edit Listing Price
```
curl -X POST "http://127.0.0.1:8000/listings/edit-price/fMrg4bMMVspwzbucAR47" \
  -d "new_price=28"
```

Delete Listing: 
```
curl -X GET  http://localhost:8000/listings/delete-listing/6QWaFwpuNrXk4KTKo5cD
```