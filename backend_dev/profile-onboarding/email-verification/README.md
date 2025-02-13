# Email Verification

## Authors: 
Roan Yeh

## Purpose:
Sends a verification email to an email with the @tufts.edu domain, 
checks a user entered verification code, and creates a profile.

TODO: 
- Check to see if email bounces (cannot reach the email)
- Make sure that email verification codes are UNIQUE!
    - Possible time expiration?
    - Check against current codes to before sending

## Necessary installs

Run command 

```
pip install -r requirements.txt  
```

## Code Login (INCLUDES email_verification!)

**Brief Description:**

Stores and retrieves a verification code from firestore database.

TODO
- Track that email has been logged (so any given email can only have one account)

**Status** 

In progress...

**Running the API**

uvicorn code_login:app --reload

**Info**

Send a verification email:
```                
curl -X 'POST' \
  http://localhost:8000/email-verification/ \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'email=Roan.Yeh@tufts.edu&password=ThisIzHandsD0wnMyFav@ppEver'
```

INPUTS: Email & password in the above json format
OUTPUTS/RESULT: Verificaton token created in database that stores code, password, and email

Verify an email (entering code):
```
curl http://localhost:8000/code_entry/<code>
```
INPUTS: Verification Code
OUTPUTS/RESULT: New profile is created!

Add Basic User Info:
```                
curl http://localhost:8000/basic-info/UuiiyHX6uWjnqHf5UqhH/Roan/Yeh/1374301 
```

## Email Verification

**Brief Description:**

Checks that the submitted email is a valid Tufts email and send a 
verification code to that address.

**Status** 

In progress...

**Running the API**

uvicorn email_verification:app --reload

**Info**

To run: 
```                
curl -X 'POST' \
  http://localhost:8000/send-code/ \
  -H 'Content-Type: application/json' \
  -d '{"email": "Roan.Yeh@tufts.edu"}'
```
