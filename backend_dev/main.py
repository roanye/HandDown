from fastapi import FastAPI
from feed_backend.swipe_functions import router as swiping_router 
from listing_api.listing_access import router as listing_router 

app = FastAPI()

app.include_router(swiping_router, prefix="/feed")

app.include_router(listing_router, prefix="/listings")

