from fastapi import APIRouter, HTTPException, Form, UploadFile, File, Body
from firebase_admin import credentials, firestore, storage
import random
import smtplib
from email.mime.text import MIMEText
from pydantic import BaseModel, EmailStr
import httpx  
from typing import TypedDict


router = APIRouter()

# =============================================================================
#                             Email Verification
# =============================================================================

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

@router.post("/send-code/")
def send_verification_code(request: EmailRequest):
    email = request.email.lower()
    if not email.endswith("@tufts.edu"):
        raise HTTPException(status_code=400, detail="Invalid email domain. Only 'tufts.edu' is allowed.")
    
    code = generate_code()
    send_email(email, code)
    print("Verification code sent successfully.")
    return {"email": email, "code": code}

# Email Verification & Storage of code in DB
@router.post("/email-verification/")
async def email_verification(email: str = Form(...), password: str = Form(...)):
    db = firestore.client()
    # Generate code and send email directly
    code = generate_code()
    send_email(email, code)
    verification_data = {
        'code': code,
        'email': email,
        'password': password
    }
    db.collection('profile-verifications').document(code).set(verification_data)
    return {"message": "Successfully stored verification data", "email": email}


# Retrieve the email and password associated with a specfic code
@router.get("/code-entry/{code}")
async def verify_email(code: str):
    """
    Verifies that the entered code is valid and retrieves the email and password associated with it.
    """
    db = firestore.client()

    code_ref = db.collection('profile-verifications').document(code)
    code_data = code_ref.get()

    if code_data.exists:
        profile_data = code_data.to_dict()
        # Create a new profile
        profile_id = create_profile(profile_data)
        # Delete verification "token" in DB
        db.collection('profile-verifications').document(code).delete()
        print("Deleted Verification")
        # Track that email has been logged (TO DO)

        return profile_data, profile_id
    else:
        raise HTTPException(status_code=404, detail="Invalid Verification Code")



# =============================================================================
#                             Profile Creation
# =============================================================================
class ProfileData(TypedDict):
    password: str
    email: str
    code: str

def create_profile(data: ProfileData):
    """
    Creates a new profile, storing uid, email, and password
    """
    db = firestore.client()

    profile_id = db.collection('profiles').document().id
    profile_data = {
        'uid': profile_id,
        'email': data['email'],
        'password': data['password']
    }

    db.collection('profiles').document(profile_id).set(profile_data)
    print(f'Created profile {profile_id}')
    return profile_id


class BasicInfo(BaseModel):
    fname: str
    lname: str
    tuftsid: str

# Add basic info: first name, last name, tuftsid
@router.post("/basic-info/{uid}")
async def add_basic_info(uid: str, info: BasicInfo):
    """
    Adds First, Last Name, and Tufts ID to Profile Info
    """
    db = firestore.client()

    profile_ref = db.collection("profiles").document(uid)
    profile_ref.set(info.dict(), merge=True)
    
    # Initialize a new empty array for interested listings
    profile_ref.set({"Interested": []}, merge=True)
    profile_ref.set({"Disliked": []}, merge=True)
    profile_ref.set({"SuperLiked": []}, merge=True)
    profile_ref.set({"Conversations": []}, merge=True)

    # Initialize a new empty array for current listings
    profile_ref.set({"Current_listings": []}, merge=True)

    return {"message": "Basic user info updated", "uid": uid}

# Upload profile photo
@router.post("/profile-photo/{uid}")
async def add_profile_photo(uid: str, image: UploadFile = File(...)):
    """
    Adds a profile photo to a profile.
    """
    db = firestore.client()
    bucket = storage.bucket('handdown-profile-photos')

    # 2. Upload the image to Firebase Storage
    image_blob = bucket.blob(f"profiles/{uid}/{image.filename}")  # Include filename for organization
    image_blob.upload_from_file(image.file)

    # 3. Store profile_photo_id in the designated profile
    profile_photo_data = {
        'imageUrl': f"https://firebasestorage.googleapis.com/v0/b/{bucket.name}/o/profiles%2F{uid}%2F{image.filename}?alt=media" 
    }
    profile_ref = db.collection("profiles").document(uid)
    profile_ref.set(profile_photo_data, merge=True)

    return {"message": "Sucessfully added profile photo.", "uid": uid}


# Add array of interests to user profile
@router.post("/profile-interests/{uid}")
async def add_user_interests(uid: str, interests: str):
    """
    Adds a list of interest badges to a profile
    """
    db = firestore.client()

    profile_ref = db.collection("profiles").document(uid)
    profile_ref.set({"interests": interests}, merge=True)

    return {"message": "Interests added", "uid": uid}

# Add array of interests to user profile
@router.post("/profile-offerings/{uid}")
async def add_user_interests(uid: str, offerings: str):
    """
    Adds a list of interest badges to a profile
    """
    db = firestore.client()

    profile_ref = db.collection("profiles").document(uid)
    profile_ref.set({"offerings": offerings}, merge=True)

    return {"message": "Offerings added", "uid": uid}
