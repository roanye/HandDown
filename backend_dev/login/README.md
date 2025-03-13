# Login

## Authors: 
Roan Yeh

## Purpose:
Allows a user to log in

## Necessary installs

Run command 

```
pip install -r requirements.txt  
```

## Account Login

**Brief Description:**

Takes email & password to log into an account.

**Status** 

In progress...

**Running the API**

uvicorn login:app --reload

**Info**

Login:
```                
curl -X 'POST' \
  http://localhost:8000/login/ \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'email=roan.yeh@tufts.edu&password=ThisIzHandsD0wnMyFav@ppEver'
```
**Note: YOU MUST INPUT EMAIL IN LOWERCASE TO MATCH THE DATABASE**

INPUTS: Email & password in the above json format
OUTPUTS/RESULT: UID to pass to front end
