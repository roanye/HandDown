from fastapi import APIRouter, Form, HTTPException
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

router = APIRouter()

@router.post("/login/")
async def login(email: str = Form(...), password: str = Form(...)):
    '''
    Logs a user into their account given an email and password
    '''
    db = firestore.client()

    email_lower = email.lower()
    # Query the database for the inputted email
    profile_ref = db.collection('profiles').where(filter=FieldFilter("email", "==", email_lower)).limit(1).stream()

    # Store that data in a documentSnap
    profile_data = next(profile_ref, None)

    # Check if a profile exists with that email
    if profile_data is None:
        raise HTTPException(status_code=401, detail="Invalid email")
    
    # Convert documentSnap to dict to access data
    profile_dict = profile_data.to_dict()

    # Check password match
    if profile_dict["password"] == password:
        return {"message": "Successfully logged in", "uid": profile_dict["uid"]}
    else:
        raise HTTPException(status_code=401, detail="Invalid password")
    
  