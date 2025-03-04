import firebase_admin
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from firebase_admin import credentials, storage, initialize_app, firestore
from typing import Optional, List
from pydantic import BaseModel
import os
from datetime import datetime
import pytz

app = FastAPI()

cred_path = '/Users/sneak100/Desktop/HandDown-creds/handdown-private-key.json'
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred, {
    'storageBucket': 'handdown-listing-photos'
})

db = firestore.client()
bucket = storage.bucket()
print(bucket)

class ListingInfo(BaseModel):
    title: str
    long_description: str
    price: int
    listing_type: str
    transaction_type: str
    tags: str
    
@app.post("/listings")
async def create_listing(
    title: str = Form(...),
    long_description: str = Form(...),
    price: int = Form(...),
    listing_type: str = Form(...),
    transaction_type: str = Form(...),
    tags: str = Form(...),
    profile_offerer_id: str = Form(...),
    image: UploadFile = File(...)
):
    """
    Creates a new listing with a title and image.
    """
    # Get time this listing was posted
    time_created = datetime.now(pytz.utc).isoformat()

    # 1. Generate a unique ID for the listing
    listing_id = db.collection("listings").document().id

    # 2. Upload the image to Firebase Storage
    image_blob = bucket.blob(f"listings/{listing_id}/{image.filename}")
    image_blob.upload_from_file(image.file)

    # 3. Create the listing dictionary
    listing_data = {
        "id": listing_id,
        "title": title,
        "long_description": long_description,
        "price": price,
        "listing_type": listing_type,
        "transaction_type": transaction_type,
        "time_created": time_created,
        "profile_offerer_id": profile_offerer_id,
        "tags": tags,
        "imageUrl": f"https://firebasestorage.googleapis.com/v0/b/{bucket.name}/o/listings%2F{listing_id}%2F{image.filename}?alt=media"
    }

    # 4. Save to Firestore
    db.collection("listings").document(listing_id).set(listing_data)

    return {"message": "Listing created successfully", "listingId": listing_id}


@app.get("/listings/{listing_id}")
async def get_listing(listing_id: str):
    """
    Retrieves a listing by its ID.
    """
    listing_ref = db.collection('listings').document(listing_id)
    listing = listing_ref.get()

    if listing.exists:
        listing_data = listing.to_dict()
        return listing_data
    else:
        raise HTTPException(status_code=404, detail="Listing not found")

@app.get("/listings")
async def get_all_listings():
    """
    Retrieves all listings.
    """
    listings = []
    for doc in db.collection('listings').stream():
        listings.append(doc.to_dict())
    return listings


@app.get("/delete-listing/{listing_id}")
async def verify_email(listing_id: str):
    """
    Deletes a listing given a listing_id
    """

    code_ref = db.collection('listings').document(listing_id)
    code_data = code_ref.get()

    if code_data.exists:
        # Delete listing in DB
        db.collection('listings').document(listing_id).delete()
        print("Deleted Listing")

        return listing_id
    else:
        raise HTTPException(status_code=404, detail="Invalid Listing")

    
# @app.put("/listings/{listing_id}")
# async def update_listing(listing_id: str, title: Optional[str] = None, image: Optional[UploadFile] = File(None)):
#     """
#     Updates an existing listing.
#     """
#     listing_ref = db.collection('listings').document(listing_id)
#     listing = listing_ref.get()

#     if listing.exists:
#         listing_data = listing.to_dict()

#         if title is not None:
#             listing_data['title'] = title

#         if image is not None:
#             # Upload the new image
#             image_blob = bucket.blob(f"listings/{listing_id}.jpg")
#             await image_blob.upload_from_file(image.file)
#             listing_data['imageUrl'] = f"https://firebasestorage.googleapis.com/v0/b/{bucket.name}/o/listings%2F{listing_id}.jpg?alt=media"

#         # Update the listing in Firestore
#         listing_ref.update(listing_data)

#         return {"message": "Listing updated successfully"}
#     else:
#         raise HTTPException(status_code=404, detail="Listing not found")

