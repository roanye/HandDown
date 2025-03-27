import requests

# List of users with associated emails and passwords
users = [
    {"email": "user1@tufts.edu", "password": "ThisIzHandsD0wnMyFav@ppEver"},
    {"email": "user2@tufts.edu", "password": "P@ssw0rd123"},
    {"email": "user3@tufts.edu", "password": "SecurePass!456"}
]

# API endpoint
url = "http://localhost:8000/email-verification/"

# Iterate through users and send POST request
for user in users:
    response = requests.post(url, data=user)

    if response.status_code == 200:
        print(f"✅ Verification email sent to {user['email']}")
    else:
        print(f"❌ Failed to send email to {user['email']}. Status: {response.status_code}, Response: {response.text}")
