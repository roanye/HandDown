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

## Profile Page

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