import firebase_admin
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from firebase_admin import credentials, storage, initialize_app, firestore
from typing import Optional
import os

app = FastAPI()

cred_path = '/Users/sneak100/Desktop/HandDown-creds/handdown-private-key.json'
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred, {
    'storageBucket': 'handdown-listing-photos'
})

db = firestore.client()
bucket = storage.bucket()
print(bucket)

@app.post("/listings")
async def create_listing(title: str = Form(...), image: UploadFile = File(...)):
    """
    Creates a new listing with a title and image.
    """
    # 1. Generate a unique ID for the listing
    listing_id = db.collection('listings').document().id

    # 2. Upload the image to Firebase Storage
    image_blob = bucket.blob(f"listings/{listing_id}/{image.filename}")  # Include filename for organization
    image_blob.upload_from_file(image.file)

    # 3. Store the listing data in Firestore
    listing_data = {
        'id': listing_id,
        'title': title,
        'imageUrl': f"https://firebasestorage.googleapis.com/v0/b/{bucket.name}/o/listings%2F{listing_id}%2F{image.filename}?alt=media"  # Construct the public URL
    }
    db.collection('listings').document(listing_id).set(listing_data)

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

# @app.delete("/listings/{listing_id}")
# async def delete_listing(listing_id: str):
#     """
#     Deletes a listing by its ID.
#     """
#     listing_ref = db.collection('listings').document(listing_id)
#     listing = listing_ref.get()

#     if listing.exists:
#         # Delete the image from Firebase Storage
#         image_blob = bucket.blob(f"listings/{listing_id}.jpg")
#         await image_blob.delete()

#         # Delete the listing from Firestore
#         listing_ref.delete()

#         return {"message": "Listing deleted successfully"}
#     else:
#         raise HTTPException(status_code=404, detail="Listing not found")
