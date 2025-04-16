from fastapi import APIRouter
from firebase_admin import credentials, firestore
import datetime

router = APIRouter()





# time_created = datetime.now(pytz.utc).isoformat()

#     # 1. Generate a unique ID for the listing
#     listing_id = db.collection("listings").document().id