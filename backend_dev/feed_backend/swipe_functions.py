import firebase_admin
from fastapi import APIRouter
from firebase_admin import credentials, firestore
from datetime import datetime
import pytz

router = APIRouter()

# Firebase setup




@router.get("/swipe-down/{listing_id}")
async def swipe_down(uid: str, listing_id: str):
    '''
    Opens conversation 
    '''
    db = firestore.client()

    # Add listing to profile's SuperLiked list -- for Mateo's algorithm
    profile_ref = db.collection('profiles').document(uid)
    profile_ref.update({"SuperLiked": firestore.ArrayUnion([listing_id])})

    # Step 0: Grab offerer's ID
    listing_ref = db.collection('listings').document(listing_id)

    listing_doc = listing_ref.get()
    offerer_id = listing_doc.get('profile_offerer_id')
    

    # Step 1: Generate conversation ID

    conversation_id = db.collection("conversations").document().id

    # Step 2: Create new conversation in DB & add necessary fields

    time_created = datetime.now(pytz.utc).isoformat()

    # Create conversation document
    messaging_data = {
            "conversation_id": conversation_id,
            "offering_user_id": offerer_id,
            "receiving_user_id": uid,
            "listing_id": listing_id,
            "time_created": time_created,
            "last_updated": time_created
    }

    db.collection("conversations").document(conversation_id).set(messaging_data)

    #         See https://docs.google.com/document/d/1MChsV3FbQ5Xd7wRlnSrGiJ8lLh0Ii70dOYyhAj9_SPE/edit?tab=t.0
    # Step 3: Add conversation ID to array in listing document

    # Add profile to listings Conversations list
    listing_ref.update({"Conversations": firestore.ArrayUnion([conversation_id])})

    # Step 4: Go to both associated profiles and add conversation ID to array

    profile_ref.update({"Conversations": firestore.ArrayUnion([conversation_id])})

    offering_profile_ref = db.collection('profiles').document(offerer_id)

    offering_profile_ref.update({"Conversations": firestore.ArrayUnion([conversation_id])})

    # Step 5: Send some arbitrary message to begin conversation

    message_time = datetime.now(pytz.utc).isoformat()
    initial_message = {
            "sender_id": uid,
            "text": "Hey, I'm interested in your listing!",
            "timestamp": message_time
    }

    # This adds the message to conversations/{conversation_id}/messages
    conversation_ref = db.collection('conversations').document(conversation_id)

    conversation_ref.collection("messages").add(initial_message)

    
    return {"message": "SUPERLIKE! Conversation started.", "uid": uid, "listing_id": listing_id} 

@router.get("/swipe-left/{listing_id}")
async def swipe_left(uid: str, listing_id: str):
    '''
    Adds listing IDs to a user's disliked listings

    TO DO: CONNECTS TO MATEO'S ALGORITHM!!!
    '''
    db = firestore.client()

    # Add listing to profile's disliked list — FOR MATEO's algo
    profile_ref = db.collection('profiles').document(uid)
    profile_ref.update({"Disliked": firestore.ArrayUnion([listing_id])})
    
    return {"message": "Not interested in this listing", "uid": uid, "listing_id": listing_id} 

@router.get("/swipe-right/{listing_id}")
async def swipe_right(uid: str, listing_id: str):
    '''
    Adds listing IDs to a user's liked listings
    * This will show in the "interested parking lot"

    TO DO: CONNECTS TO MATEO'S ALGORITHM!!!
    '''
    db = firestore.client()

    # Add listing to profile's interested parking lot
    profile_ref = db.collection('profiles').document(uid)
    profile_ref.update({"Interested": firestore.ArrayUnion([listing_id])})

    # Add profile to listings interested users
    listing_ref = db.collection('listings').document(listing_id)
    listing_ref.update({"Interested_users": firestore.ArrayUnion([uid])})

    return {"message": "Interested in this listing", "uid": uid, "listing_id": listing_id} 

'''
Note: Swipe up simply displays more info on listing. This will be done on the 
front end.
'''
