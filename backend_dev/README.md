# Backend Dev

## Authors: 
Roan Yeh & Mateo Sufuentes

## Purpose:
Constitutes the backend of the marketplace. Has subdirectories for 
the recommendation algorithm and other backend APIs to connect to database and 
other infrastructure. 

## Listing Access

<u>Brief Description:</u> 
Defines post and get functions to read and write listings.

<u>Status</u> In progress...

<u>Info</u>
Create Listing:
```
curl -X POST -H "Content-Type: multipart/form-data" -F "title=My New Listing" -F "image=@path/to/image.jpg" http://localhost:8000/listings
```

Get Listing:
```
curl http://localhost:8000/listings/listing_id
```

Get all Listings:
```
curl http://localhost:8000/listings
```

Update Listing:
```
curl -X PUT -H "Content-Type: multipart/form-data" -F "title=Updated Title" -F "image=@path/to/new_image.jpg" http://localhost:8000/listings/listing_id
```

Delete Listing:
```
curl -X DELETE http://localhost:8000/listings/listing_id
```





