# HandDown

A college marketplace app — students list, swipe on, and message each other about items for sale.

## Repo structure

```
HandDown/
├── backend_dev/      FastAPI backend, mounted on Firebase (Firestore + Storage)
└── frontend_dev/      Expo / React Native app
```

## Backend (`backend_dev/`)

FastAPI app, entry point at `backend_dev/main.py`, run with:

```
cd backend_dev
pip install -r requirements.txt
uvicorn main:app --reload
```

It expects a Firebase service account key on disk **outside the repo**, at a path
hardcoded in `main.py` (`cred_path`). You'll need to point this at your own
Firebase project's key, or ask a maintainer for the dev credentials file — it is
intentionally never committed to git.

Each feature lives in its own module, mounted as a router with its own prefix.
Full curl examples for every endpoint are in `backend_dev/README.md`; short version:

| Module | Prefix | Purpose |
|---|---|---|
| `feed_backend/` | `/feed` | Swipe right/left/up/down on listings |
| `listing_api/` | `/listings` | Create, edit, fetch, delete listings |
| `login/` | `/login` | Login |
| `profile_onboarding/` | `/onboarding` | Signup, email verification, profile setup |
| `profile_page/` | `/profile` | Profile read/edit |
| `messaging/` | `/conversations` | Conversations and messages between users |
| `algo/` | `/algo` | Feed ranking and search |
| `test_files/` | `/clear` | Admin-only test/reset utilities |

Each module folder has its own `README.md` and `requirements.txt` with more detail.

## Frontend (`frontend_dev/Handdown_Frontend/`)

Expo-managed React Native app (Expo Router, NativeWind/Tailwind for styling).

```
cd frontend_dev/Handdown_Frontend
npm install
npm start      # then choose iOS / Android / web from the Expo CLI
```

Screens live under `app/` (feed, listings, messaging, profile, onboarding flow).

### ⚠️ Frontend is behind — expect things not to line up

The frontend code in this repo is **not the latest version**. Newer frontend work
exists locally on a contributor's machine and has not yet been committed/pushed to
GitHub. Practically, that means:

- Some backend endpoints described above may not have a matching screen/call in
  this repo's frontend yet, or the frontend may call something slightly different
  from what's currently live on `main`.
- If you pull this repo expecting it to match what you've seen demoed or
  discussed, the UI/flows here may be a step or two behind.

If you're the one with the newer frontend code locally: push it to a branch and
open a PR rather than letting it drift further from `main` — the longer it sits
unpushed, the harder this gets to reconcile.

## Branches

`main` is the integration branch. There are a number of other branches on the
remote (`backend_dev`, `frontend_dev`, `backend_docker`, `cloud-scripts`,
`proof-of-concept`, etc.) representing earlier work-in-progress splits of the
project before things were consolidated under `backend_dev/` and
`frontend_dev/` — most are stale and already merged in spirit, not actively
developed.

## Status

Early/active development. Expect rough edges, missing error handling, and the
frontend/backend sync issue noted above.
