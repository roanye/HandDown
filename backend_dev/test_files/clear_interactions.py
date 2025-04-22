from fastapi import APIRouter, HTTPException
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from typing import Optional, List
import os

router = APIRouter()

@router.get("/clear-interactions")
async def clear_interactions():
    db = firestore.client()

    # CLEAR PROFILE INTERACTIONS
    profiles_ref = db.collection('profiles')
    docs = profiles_ref.stream()

    for doc in docs:
        data = doc.to_dict()
        updates = {}

        for key, value in data.items():
            if isinstance(value, list) and key != "Current_listings":
                updates[key] = []

            if updates:
                profiles_ref.document(doc.id).update(updates)
                print(f"Updated profile {doc.id} with empty lists for: {list(updates.keys())}")
    
    # CLEAR LISTING INTERACTIONS
    listings_ref = db.collection('listings')
    docs = listings_ref.stream()

    for doc in docs:
        data = doc.to_dict()
        updates = {}

        for key, value in data.items():
            if isinstance(value, list):
                updates[key] = []

            if updates:
                listings_ref.document(doc.id).update(updates)
                print(f"Updated listing {doc.id} with empty lists for: {list(updates.keys())}")
    
    
    # DELETE CONVERSATIONS
    conversations_ref = db.collection('conversations')
    docs = conversations_ref.stream()

    for doc in docs:
        if doc.id != "conversaton_id":
            messages_ref = conversations_ref.document(doc.id).collection('messages')

            batch = db.batch()
            for message in messages_ref.stream():
                batch.delete(message.reference)

            batch.commit()

            # Delete the conversation document
            conversations_ref.document(doc.id).delete()
            print(f"Deleted conversation: {doc.id}")


    return {"Message": "Cleared all interaction data!"}


