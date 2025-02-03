# Email Verification

## Authors: 
Roan Yeh

## Purpose:
Sends a verification email to an email with the @tufts.edu domain.

TODO: Check to see if email bounces (cannot reach the email)

## Email Verification

**Brief Description:**

Checks that the submitted email is a valid Tufts email and send a 
verification code to that address.

**Status** 

In progress...

**Necessary installs**

Run command 

```
pip install -r requirements.txt  
```

**Running the API**

uvicorn listing-access:app --reload

**Info**

To run: 
```                
curl -X 'POST' \
  http://localhost:8000/send-code/ \
  -H 'Content-Type: application/json' \
  -d '{"email": "Roan.Yeh@tufts.edu"}'
```