# Profile Page

## Authors: 
Roan Yeh

## Purpose:
Allow for the access of profile information

## Necessary installs

Run command 

```
pip install -r requirements.txt  
```

## Profile Page

**Brief Description:**
Simply retrieves all profile information given a profile ID

**Status** 

In progress...

**Running the API**

uvicorn profile_page:app --reload

**Info**

Profile Access
```
curl http://localhost:8000/profile-access/profile_id
```

Get All Profiles
```
curl http://localhost:8000/profiles
```

Get All Profiles
```
curl http://localhost:8000/profiles/get-profile-offerings/{profile_id}
```
