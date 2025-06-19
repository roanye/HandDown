from fastapi import APIRouter
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from datetime import datetime
import pytz
from pydantic import BaseModel

router = APIRouter()

@router.get("/get-all-conversations/{profile_id}")
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

class MessageBody(BaseModel):
    message_contents: str

@router.post("/send-message/{conversation_id}/{profile_id}")
async def send_message(conversation_id: str, profile_id: str, body: MessageBody):
    message_contents = body.message_contents
    db = firestore.client()

    conversation_ref = db.collection('conversations').document(conversation_id)
    conversation_data = conversation_ref.get()


    # Update conversaton -- last_updated

    time_sent = datetime.now(pytz.utc).isoformat()

    message = {
            "sender_id": profile_id,
            "text": message_contents,
            "timestamp": time_sent
    }

    # This adds the message to conversations/{conversation_id}/messages
    conversation_ref = db.collection('conversations').document(conversation_id)

    conversation_ref.collection("messages").add(message)

    if conversation_data.exists:
        conversation_ref.set({"last_updated": time_sent}, merge=True)

        return {"message": f"Successfully sent message from {profile_id}!", "time_sent": time_sent}

    return {"message": "ERROR -- converation does not exist!"}


@router.get("/get-all-messages/{conversation_id}")
async def get_all_messages(conversation_id: str):
    db = firestore.client()

    conversation_ref = db.collection('conversations').document(conversation_id).collection('messages')
    conversation_data = conversation_ref.stream()

    results = [doc.to_dict() for doc in conversation_data]

    results.sort(key=lambda x: x.get("timestamp"), reverse=True)

    return results

@router.get("/delete-conversation/{conversation_id}")
async def delete_conversation(conversation_id: str):
    db = firestore.client()

    conversation_ref = db.collection('conversations').document(conversation_id)
    conversation_data = conversation_ref.get()
    conversation_dict = conversation_data.to_dict()

    profile1_ref = db.collection('profiles').document(conversation_dict['offering_user_id'])

    profile1_ref.update({
        "Conversations": firestore.ArrayRemove([conversation_id])
    })

    profile2_ref = db.collection('profiles').document(conversation_dict['receiving_user_id'])

    profile2_ref.update({
        "Conversations": firestore.ArrayRemove([conversation_id])
    })

    # Batch delete messages
    messages_ref = conversation_ref.collection('messages')

    batch = db.batch()
    for message in messages_ref.stream():
        batch.delete(message.reference)

    batch.commit()

    if conversation_data.exists:
        conversation_ref.delete()
    
    return {"message": f"Successfully deleted conversation {conversation_id}"}
    