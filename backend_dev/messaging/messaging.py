from fastapi import APIRouter
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
import datetime

router = APIRouter()

@router.post("/get-all-conversations/{profile_id}")
async def get_all_conversations(profile_id: str):
    # Step 1: Get profile info

    db = firestore.client()

    # Add listing to profile's interested parking lot

    conversation_ref = db.collection('conversations')

    query_ref1 = conversation_ref.where(filter=FieldFilter('offering_user_id', '==', profile_id)).stream()

    query_ref2 = conversation_ref.where(filter=FieldFilter('receiving_user_id', '==', profile_id)).stream()

    results = [doc.to_dict() for doc in query_ref1] + [doc.to_dict() for doc in query_ref2]

    results.sort(key=lambda x: x.get("last_updated"), reverse=True)


    return results
    

# time_created = datetime.now(pytz.utc).isoformat()

#     # 1. Generate a unique ID for the listing
#     listing_id = db.collection("listings").document().id


# @router.post("send-message/{profile_id}")
# async def send_message

# Update last-updated filed in conversation document
# Add a new message to conversation messages collection
