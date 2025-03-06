import firebase_admin
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from firebase_admin import credentials, storage, initialize_app, firestore
from typing import Optional, List
import os

app = FastAPI()

# Firebase setup
cred_path = '/Users/sneak100/Desktop/HandDown-creds/handdown-private-key.json'
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred, {
    'storageBucket': 'handdown-profile-photos'
})

db = firestore.client()
bucket = storage.bucket()
print(bucket)

@app.get("/profile-access/{profile_id}")
async def get_profile(profile_id: str):
    """
    Retrieves a profile by its ID.
    """
    profile_ref = db.collection('profiles').document(profile_id)
    profile = profile_ref.get()

    if profile.exists:
        profile_data = profile.to_dict()
        return profile_data
    else:
        raise HTTPException(status_code=404, detail="Profile not found")