import firebase_admin
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from firebase_admin import credentials, storage, initialize_app, firestore
from typing import Optional, List
from pydantic import BaseModel

app = FastAPI()

# Firebase setup
cred_path = '/Users/sneak100/Desktop/HandDown-creds/handdown-private-key.json'
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

db = firestore.client()


@app.get("/swipe-down/{listing_id}")
async def swipe_down(profile_id: str, listing_id: str):
        '''
        Opens conversation 
        '''
        print(listing_id)
        # THIS IS TO BE DONE LATER!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        # Step 1: Generate conversation ID
        # Step 2: Create new conversation in DB & add necessary fields
        #         See https://docs.google.com/document/d/1MChsV3FbQ5Xd7wRlnSrGiJ8lLh0Ii70dOYyhAj9_SPE/edit?tab=t.0
        # Step 3: Add conversation ID to array in listing document
        # Step 4: Go to both associated profiles and add conversation ID to array
        # Step 5: Send some arbitrary message to begin conversation (add this to an array in conversation document)
        #         - Make sure formatting is correct: "R:" - receiving, "O:" - offering


@app.get("/swipe-left/{listing_id}")
async def swipe_left(uid: str, listing_id: str):
        '''
        Adds listing IDs to a user's disliked listings

        TO DO: CONNECTS TO MATEO'S ALGORITHM!!!
        '''
        
        return {"message": "Not interested in this listing", "uid": uid, "listing_id": listing_id} 

@app.get("/swipe-right/{listing_id}")
async def swipe_right(uid: str, listing_id: str):
        '''
        Adds listing IDs to a user's liked listings
        * This will show in the "interested parking lot"

        TO DO: CONNECTS TO MATEO'S ALGORITHM!!!
        '''

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
