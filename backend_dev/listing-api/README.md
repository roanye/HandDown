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

uvicorn, fastapi, firebase-admin

**Running the API**

uvicorn listing-access:app --reload

**Info**

Create Listing:
```
curl -X POST \
-H "Content-Type: multipart/form-data" \
-F "title=Logo" \
-F "image=@/Users/sneak100/Desktop/HandDown/backend_dev/listing-api/test-images/handdown.png" \
http://localhost:8000/listings
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
curl -X DELETE http://localhost:8000/listings/listing_id
```





