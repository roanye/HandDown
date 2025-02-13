import firebase_admin
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from firebase_admin import credentials, storage, initialize_app, firestore
from typing import Optional
import os

app = FastAPI()

cred_path = '/Users/sneak100/Desktop/HandDown-creds/handdown-private-key.json'
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

db = firestore.client()

@app.post("/basic-info/{uid}")
async def add_basic_info(uid: str = Form(...), fname: str = Form(...), 
                         lname: str = Form(...), tuftsid: str = Form(...)):
    """
    Adds First, last name, and tufts id to profile info
    """

    # Retrieve document w/ profile
    profile_ref = db.collection("profiles").document(uid)

    # Set fields to new values
    profile_ref.set({"fname": fname}, merge=True)
    profile_ref.set({"lname": lname}, merge=True)
    profile_ref.set({"tuftsid": tuftsid}, merge=True)

    return {"message": "Basic user info updated", "uid": uid}
