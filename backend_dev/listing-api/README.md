# Listing API

## Authors: 
Roan Yeh

## Purpose:
Creates a listing with basic information, accesses a specific listing by ID, 
deletes a listing, and accesses all listings.

TODO: ADD MORE INFORMATION/ATTRIBUTES!

## Listing Access

**Brief Description:**

Defines post and get functions to read and write listings.

**Status** 

In progress...

**Necessary installs**

uvicorn, fastapi, firebase-admin, pytz

**Running the API**

uvicorn listing-access:app --reload

**Info**

Create Listing:
```
curl -X POST "http://127.0.0.1:8000/listings" \
  -H "Content-Type: multipart/form-data" \
  -F "title=Banama" \
  -F "long_description=A classic vintage banama in excellent condition." \
  -F "price=27" \
  -F "listing_type=listing" \
  -F "transaction_type=sell" \
  -F "tags=home decor" \
  -F "image=@/Users/sneak100/Desktop/HandDown/backend_dev/listing-api/test-images/banama.jpeg"
```

Get Listing:
```
curl http://localhost:8000/listings/listing_id
```

Get all Listings:
```
curl http://localhost:8000/listings
```

Update Listing: NOT IMPLEMENTED AS OF NOW
```
curl -X PUT -H "Content-Type: multipart/form-data" -F "title=Updated Title" -F "image=@path/to/new_image.jpg" http://localhost:8000/listings/listing_id
```

Delete Listing: NOT IMPLEMENTED AS OF NOW
```
curl -X GET  http://localhost:8000/delete-listing/6QWaFwpuNrXk4KTKo5cD
```







