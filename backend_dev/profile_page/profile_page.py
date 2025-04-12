import firebase_admin
from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from firebase_admin import credentials, storage, initialize_app, firestore
from typing import Optional, List
import os

router = APIRouter()



@router.get("/profile-access/{profile_id}")
async def get_profile(profile_id: str):
    """
    Retrieves a profile by its ID.
    """
    db = firestore.client()

    profile_ref = db.collection('profiles').document(profile_id)
    profile = profile_ref.get()

    if profile.exists:
        profile_data = profile.to_dict()

        return profile_data
    else:
        raise HTTPException(status_code=404, detail="Profile not found")


@router.get("/profiles")
async def get_all_profiles():
    """
    Retrieves all listings.
    """
    db = firestore.client()
    profiles = []
    for doc in db.collection('profiles').stream():
        profiles.append(doc.to_dict())
    return profiles