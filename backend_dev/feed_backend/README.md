# Feed-backend

## Authors: 
Roan Yeh

## Purpose:
Adds functionality to swiping on the feed:

1. Up — "More...": Shows long description of listing
2. Down — "Super like": Opens a new message window 
3. Left — "Dislike": Dislike photo —-> effects algorithm
4. Right — "Like": Move listing into profile's "liked parking lot"

## Necessary installs

Run command 

```
pip install -r requirements.txt  
```

## Swipe functions

**Brief Description:**

Defines the actions for each swipe direction (see descriptions above in purpose section)

**Status** 

In progress...

**Running the API**

uvicorn swipe_functions:app --reload

**Info**

Swipe Right:
```
curl -X 'GET' \
  'http://localhost:8000/swipe-right/ucEe1I7S5I2NeMEaAXsd?uid=kqPhYvDW6b4fSmmzD1or'
```

Swipe Left:


Swipe Down:


