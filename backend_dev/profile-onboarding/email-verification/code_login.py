import firebase_admin
from fastapi import FastAPI, HTTPException, Form
from firebase_admin import credentials, firestore
import os
import random
import smtplib
from email.mime.text import MIMEText
from pydantic import BaseModel, EmailStr
import httpx  
from typing import TypedDict


app = FastAPI()

# Firebase setup
cred_path = '/Users/sneak100/Desktop/HandDown-creds/handdown-private-key.json'
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

db = firestore.client()

# Gmail SMTP settings 
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "handdown.downhand@gmail.com"
SMTP_PASSWORD = "iuvx dxjl jyax ywca"

# Email verification
class EmailRequest(BaseModel):
    email: EmailStr

def generate_code() -> str:
    '''Generates a random 6-digit code'''
    return str(random.randint(100000, 999999))

def send_email(email: str, code: str):
    '''Sends an email with a verification code'''
    subject = "Your Verification Code"
    body = f"Your verification code is: {code}"
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SMTP_USERNAME
    msg["To"] = email
    
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SMTP_USERNAME, email, msg.as_string())
    except smtplib.SMTPException as e:
        raise HTTPException(status_code=500, detail=f"Email sending failed: {str(e)}")

@app.post("/send-code/")
def send_verification_code(request: EmailRequest):
    email = request.email.lower()
    if not email.endswith("@tufts.edu"):
        raise HTTPException(status_code=400, detail="Invalid email domain. Only 'tufts.edu' is allowed.")
    
    code = generate_code()
    send_email(email, code)
    print("Verification code sent successfully.")
    return {"email": email, "code": code}

# Email Verification & Storage of code in DB
@app.post("/email-verification/")
async def email_verification(email: str = Form(...), password: str = Form(...)):
    """Handles email verification and stores data with Firebase"""
    url = "http://localhost:8000/send-code/"
    data = {"email": email}

    async with httpx.AsyncClient() as client:  # Using async httpx client
        response = await client.post(url, json=data)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to send verification email")

    response_data = response.json()  # Access the response as JSON
    print(response_data)
    verification_data = {
        'code': response_data["code"],
        'email': response_data["email"],
        'password': password
    }

    db.collection('profile-verifications').document(response_data["code"]).set(verification_data)
    
    return {"message": "Successfully stored verification data", "email": response_data["email"]}

# Retrieve the email and password associated with a specfic code
@app.get("/code-entry/{code}")
async def verify_email(code: str):
    """
    Verifies that the entered code is valid and retrieves the email and password associated with it.
    """

    code_ref = db.collection('profile-verifications').document(code)
    code_data = code_ref.get()

    if code_data.exists:
        profile_data = code_data.to_dict()
        # Create a new profile
        create_profile(profile_data)
        # Delete verification "token" in DB
        db.collection('profile-verifications').document(code).delete()
        print("Deleted Verification")
        # Track that email has been logged (TO DO)

        return profile_data
    else:
        raise HTTPException(status_code=404, detail="Invalid Verification Code")

class ProfileData(TypedDict):
    password: str
    email: str
    code: str

def create_profile(data: ProfileData):
    """
    Creates a new profile, storing uid, email, and password
    """
    profile_id = db.collection('profiles').document().id
    profile_data = {
        'uid': profile_id,
        'email': data['email'],
        'password': data['password']
    }

    db.collection('profiles').document(profile_id).set(profile_data)
    print(f'Created profile {profile_id}')
