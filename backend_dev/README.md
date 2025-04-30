# Backend Dev — API Scripts

## Authors: 
Roan Yeh

## Purpose:
Serves as the endpoint for all API calls

## Necessary installs

Run command 

```
pip install -r requirements.txt  
```

**Brief Description:**
All API calls are mounted here to run through on endpoint.

**Status** 

In progress...

**Running the API**

uvicorn main:app --reload

**Info**

*Feed*
--------
Swipe right: 
```
curl -X 'GET' \
  'http://localhost:8000/feed/swipe-right/<listing-id>?uid=<uid>'
```

Swipe left:
```
curl -X 'GET' \
  'http://localhost:8000/feed/swipe-left/<listing-id>?uid=<uid>'
```

Swipe down:
```
curl -X 'GET' \
  'http://localhost:8000/feed/swipe-down/<listing-id>?uid=<uid>'
```


*Listings*
--------

Create Listing:
```
curl -X POST "http://127.0.0.1:8000/listings/create-listing" \
  -H "Content-Type: multipart/form-data" \
  -F "title=Banama" \
  -F "long_description=A classic vintage banama in excellent condition." \
  -F "price=27" \
  -F "listing_type=listing" \
  -F "transaction_type=sell" \
  -F "profile_offerer_id=M1TvCTanfGUlLeTYw3NP" \
  -F "tags=home decor" \
  -F "image=@/Users/sneak100/Desktop/HandDown/backend_dev/listing_api/test-images/banama.jpeg"
```

Get Listing:
```
curl http://localhost:8000/listings/get-listing/listing_id
```

Get all Listings:
```
curl http://localhost:8000/listings/get-all-listings
```

Edit Listing Title:
```
curl -X POST "http://127.0.0.1:8000/listings/edit-listing-title/fMrg4bMMVspwzbucAR47" \
  -d "new_title=Barama"
```

Edit Listing Description:
```
curl -X POST "http://127.0.0.1:8000/listings/edit-listing-description/fMrg4bMMVspwzbucAR47" \
  -d "new_desc=I don't really know what this is but you want it"
```

Edit Listing Price:
```
curl -X POST "http://127.0.0.1:8000/listings/edit-price/fMrg4bMMVspwzbucAR47" \
  -d "new_price=28"
```

Delete Listing: 
```
curl -X GET  http://localhost:8000/listings/delete-listing/6QWaFwpuNrXk4KTKo5cD
```

*Login*
--------

Login:
```                
curl -X 'POST' \
  http://localhost:8000/login/login/ \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'email=Roan.Yeh@tufts.edu&password=ThisIzHandsD0wnMyFav@ppEver'
```

*Onboarding*
--------

Send a verification email:
```                
curl -X 'POST' \
  http://localhost:8000/onboarding/email-verification/ \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'email=Roan.Yeh@tufts.edu&password=GoFastaP@sta'
```

INPUTS: Email & password in the above json format
OUTPUTS/RESULT: Verificaton token created in database that stores code, password, and email

Verify an email (entering code):
```
curl http://localhost:8000/onboarding/code-entry/<code>
```
INPUTS: Verification Code
OUTPUTS/RESULT: New profile is created!

Add Basic User Info:
```                
curl -X 'POST' 'http://localhost:8000/onboarding/basic-info/UuiiyHX6uWjnqHf5UqhH' \
  -H 'Content-Type: application/json' \
  -d '{"fname": "Roan", "lname": "Yeh", "tuftsid": "1374301"}'
```

Add Profile Photo:
```                
curl -X 'POST' \
  http://localhost:8000/onboarding/profile-photo/UuiiyHX6uWjnqHf5UqhH \
  -F "image=@/Users/sneak100/Desktop/HandDown/backend_dev/listing_api/test-images/handdown.png"
```
Add Interests:
```
curl -X 'POST' \
  'http://localhost:8000/onboarding/profile-interests/UuiiyHX6uWjnqHf5UqhH?interests=Books%20Clothes%20Accessories' \
  -H 'Content-Type: application/json'

```

Add Offerings:
```
curl -X 'POST' \
  'http://localhost:8000/onboarding/profile-offerings/UuiiyHX6uWjnqHf5UqhH?offerings=Books%20Clothes%20Accessories' \
  -H 'Content-Type: application/json'
```

*Profile Page*
--------

Profile Access:
```
curl http://localhost:8000/profile/profile-access/<profile_id>
```

Public Profile Access:
```
curl http://localhost:8000/profile/public-profile-access/{profile_id}
```

Get All Profiles:
```
curl http://localhost:8000/profile/profiles
```

Get Profile Offerings:
```
curl http://localhost:8000/profile/get-profile-offerings/{profile_id}
```

Remove Interested Listing:
```
curl -X 'GET' \
  'http://localhost:8000/profile/remove-interested/<listing-id>?uid=<uid>'
```

*Conversations*

Get all Conversations:
```
curl -X 'GET' \
  'http://localhost:8000/conversations/get-all-conversations/{profile_id}'
```

Send Message:
```
curl -X POST \
  http://localhost:8000/conversations/send-message/{conversaton_id}/{profile_id} \
  -H "Content-Type: application/json" \
  -d '{"message_contents": "hey whats up"}'
```

Get all Messages:
```
curl -X 'GET' \
  'http://localhost:8000/conversations/get-all-messages/{conversation_id}'
```

Delete Conversation:
```
curl -X 'GET' \
  'http://localhost:8000/conversations/delete-conversation/{conversation_id}'
```

*Algo*

Get feed:
```
curl -X 'GET' \
  'http://localhost:8000/algo/get-feed-listings/{uid}'
```

Get search results:
```
curl -X 'GET' \
  'http://localhost:8000/algo/get-search-listings/{prompt}?profile_id=<uid>'
```

*Testing Files -- ADMIN ONLY*

Clear Interactions:
```
curl -X 'GET' \
  'http://localhost:8000/clear/clear-interactions'
```
