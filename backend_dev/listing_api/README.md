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

Run command 

```
pip install -r requirements.txt  
```

**Running the API**

uvicorn listing_access:app --reload

**Info**

Create Listing:
```
curl -X POST "http://127.0.0.1:8000/create-listing" \
  -H "Content-Type: multipart/form-data" \
  -F "title=Banama" \
  -F "long_description=A classic vintage banama in excellent condition." \
  -F "price=27" \
  -F "listing_type=listing" \
  -F "transaction_type=sell" \
  -F "profile_offerer_id=M1TvCTanfGUlLeTYw3NP" \
  -F "tags=home decor" \
  -F "image=@/Users/sneak100/Desktop/HandDown/backend_dev/listing-api/test-images/banama.jpeg"
```

Get Listing:
```
curl http://localhost:8000/get-listing/listing_id
```

Get all Listings:
```
curl http://localhost:8000/get-all-listings
```

Edit Listing Title
```
curl -X POST "http://127.0.0.1:8000/edit-listing-title/fMrg4bMMVspwzbucAR47" \
  -d "new_title=Barama"
```

Edit Listing Description
```
curl -X POST "http://127.0.0.1:8000/edit-listing-description/fMrg4bMMVspwzbucAR47" \
  -d "new_desc=I don't really know what this is but you want it"
```

Edit Listing Price
```
curl -X POST "http://127.0.0.1:8000/edit-price/fMrg4bMMVspwzbucAR47" \
  -d "new_price=28"
```

Delete Listing: 
```
curl -X GET  http://localhost:8000/delete-listing/6QWaFwpuNrXk4KTKo5cD
```







