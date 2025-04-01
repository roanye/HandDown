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
        "Interested_users": [],
        "imageUrl": f"https://firebasestorage.googleapis.com/v0/b/{bucket.name}/o/listings%2F{listing_id}%2F{image.filename}?alt=media"
    }

    # 4. Save to Firestore
    db.collection("listings").document(listing_id).set(listing_data)
    
    # 5. Add listing to profile offer's informaton
    profile_ref = db.collection("profiles").document(profile_offerer_id)

    profile_ref.update({"Current_listings": firestore.ArrayUnion([listing_id])})

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
async def delete_listing(listing_id: str):
    """
    Deletes a listing given a listing_id
    """

    # TO DO: 
    # - delete all messages related to listing
    # - delete all mentions of listing ID in other profiles


    listing_ref = db.collection('listings').document(listing_id)
    listing_data = listing_ref.get()

    if listing_data.exists:
        # Delete listing in DB
        db.collection('listings').document(listing_id).delete()
        print("Deleted Listing")

        return listing_id
    else:
        raise HTTPException(status_code=404, detail="Invalid Listing")


@app.post("/edit-listing-title/{listing_id}")
async def edit_listing_title(listing_id: str, new_title: str = Form(...)):
    listing_ref = db.collection('listings').document(listing_id)
    listing_data = listing_ref.get()

    if listing_data.exists:
        # Delete listing in DB
        listing_ref.set({"title": new_title}, merge=True)
        print("Changed title for", listing_id, "to", new_title, "!")

        return listing_id
    else:
        raise HTTPException(status_code=404, detail="Invalid Listing")
    
@app.post("/edit-listing-description/{listing_id}")
async def edit_listing_description(listing_id: str, new_desc: str = Form(...)):
    listing_ref = db.collection('listings').document(listing_id)
    listing_data = listing_ref.get()

    if listing_data.exists:
        # Delete listing in DB
        listing_ref.set({"long_description": new_desc}, merge=True)
        print("Changed title for", listing_id, "to", new_desc, "!")

        return listing_id
    else:
        raise HTTPException(status_code=404, detail="Invalid Listing")
    
@app.post("/edit-price/{listing_id}")
async def edit_listing_description(listing_id: str, new_price: str = Form(...)):
    listing_ref = db.collection('listings').document(listing_id)
    listing_data = listing_ref.get()

    if listing_data.exists:
        # Delete listing in DB
        listing_ref.set({"price": new_price}, merge=True)
        print("Changed price for", listing_id, "to", new_price, "!")

        return listing_id
    else:
        raise HTTPException(status_code=404, detail="Invalid Listing")
        

