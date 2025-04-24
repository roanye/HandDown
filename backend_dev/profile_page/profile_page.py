from fastapi import APIRouter, HTTPException
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

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
    Retrieves all profiles.
    """
    db = firestore.client()
    profiles = []
    for doc in db.collection('profiles').stream():
        profiles.append(doc.to_dict())
    return profiles

@router.get("/get-profile-offerings/{profile_id}")
async def get_profile_offerings(profile_id: str):
    """
    Retrieves all listings offered by a specific profile.
    """
    db = firestore.client()
    
    listing_ref = db.collection('listings')

    query_ref = listing_ref.where(filter=FieldFilter('profile_offerer_id', '==', profile_id))

    
    query_doc = query_ref.stream()

    query_result = [doc.to_dict() for doc in query_doc]

    return query_result

@router.get("/remove-interested/{listing_id}")
async def remove_interested(uid: str, listing_id: str):
    '''
    Removes listing from interested parking lot
    '''
    db = firestore.client()
    profile_ref = db.collection('profiles').document(uid)

    # Update rating
    profile_ref.update({
        "Interested": firestore.ArrayRemove([listing_id])
    })
    
    return {"message": "No longer intersted in this listing!", "uid": uid, "listing_id": listing_id} 
