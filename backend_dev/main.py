from fastapi import FastAPI
import firebase_admin
from firebase_admin import credentials, storage, firestore
from feed_backend.swipe_functions import router as swiping_router 
from listing_api.listing_access import router as listing_router 
from profile_onboarding.email_verification.code_login import router as onboarding_router 
from profile_page.profile_page import router as profile_router 

from login.login import router as login_router 

app = FastAPI()

# Firebase setup

cred_path = '/Users/sneak100/Desktop/HandDown-creds/handdown-private-key.json'
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred, {
    'storageBucket': 'handdown-listing-photos'
})

app.include_router(swiping_router, prefix="/feed")

app.include_router(listing_router, prefix="/listings")

app.include_router(login_router, prefix="/login")

app.include_router(onboarding_router, prefix="/onboarding")

app.include_router(profile_router, prefix="/profile")

