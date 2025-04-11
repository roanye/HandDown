from fastapi import FastAPI
from feed_backend.swipe_functions import router as swiping_router 

app = FastAPI()
app.include_router(swiping_router, prefix="/feed")
