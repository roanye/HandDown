import requests

BASE_URL = "http://localhost:8000"

users = [
    {"email": "user1@tufts.edu", 
     "password": "ThisIzHandsD0wnMyFav@ppEver",
     "fname": "Murtle",
     "lname": "Binks",
     "code": "555250",
     "tuftsid": "1234567",
     "profile_photo": "/Users/sneak100/Desktop/HandDown/backend_dev/listing-api/test-images/banama.jpeg",
     "interests": "Costumes Outdoor Bedding",
     "profile_id": "M1TvCTanfGUlLeTYw3NP",
     "offerings": "Groceries Transportation Housing"},
    {"email": "user2@tufts.edu", 
     "password": "P@ssw0rd123",
     "fname": "Bradley",
     "lname": "Miggs",
     "code": "557642",
     "tuftsid": "7654321",
     "profile_photo": "/Users/sneak100/Desktop/HandDown/backend_dev/listing-api/test-images/travisfish.jpeg",
     "interests": "Books Housing Bedding",
     "profile_id": "k6nJjcACWnJcjqwM7emT",
     "offerings": "Groceries Outdoor Costumes"},
    {"email": "user3@tufts.edu", 
     "password": "SecurePass!456",
     "fname": "Marge",
     "lname": "Meddlesticks",
     "code": "560551",
     "tuftsid": "7654321",
     "profile_photo": "/Users/sneak100/Desktop/HandDown/backend_dev/listing-api/test-images/IMG_4723.png",
     "interests": "Books Electronics Clothes",
     "profile_id": "Ez132wSnapZPOqKFCsgi",
     "offerings": "Kitchenware Outdoor Furniture"}
]


def verify_email(code):
    """Verifies email using the provided verification code"""
    response = requests.get(f"{BASE_URL}/code-entry/{code}")
    if response.status_code == 200:
        profile_info = response.text.strip()  # Assuming API returns profile ID as response
        profile_id = profile_info[1]
        print(f"✅ Email verified! Profile ID: {profile_id}")
        return profile_id
    else:
        print(f"❌ Email verification failed for code {code}. Status: {response.status_code}, Response: {response.text}")
        return None
    
def add_basic_info(profile_id, fname, lname, tuftsid):
    """Adds basic user info"""

    data = {"fname": fname, "lname": lname, "tuftsid": tuftsid}
    response = requests.post(f"{BASE_URL}/basic-info/{profile_id}", json=data)
    if response.status_code == 200:
        print(f"✅ Basic info added for {fname} {lname}") 
    else: 
        print(f"❌ Failed to add basic info: {response.text}")

def upload_profile_photo(profile_id, photo_path):
    """Uploads profile photo"""
    with open(photo_path, "rb") as image:
        files = {"image": image}
        response = requests.post(f"{BASE_URL}/profile-photo/{profile_id}", files=files)
        
        if response.status_code == 200:
            print(f"✅ Profile photo uploaded for {profile_id}") 
        else:
            print(f"❌ Failed to upload photo: {response.text}")

def add_interests(profile_id, interests):
    """Adds user interests"""
    response = requests.post(f"{BASE_URL}/profile-interests/{profile_id}?interests={interests.replace(' ', '%20')}")

    
    if response.status_code == 200:
        print(f"✅ Interests added for {profile_id}") 
    else:
        print(f"❌ Failed to add interests: {response.text}")

def add_offerings(profile_id, offerings):
    """Adds user offerings"""
    response = requests.post(f"{BASE_URL}/profile-offerings/{profile_id}?offerings={offerings.replace(' ', '%20')}")
    
    if response.status_code == 200: 
        print(f"✅ Offerings added for {profile_id}") 
    else: 
        print(f"❌ Failed to add offerings: {response.text}")

# Process each user
for user in users:
    print(f"\n🚀 Processing {user['email']}...")

    # # Step 1: Verify Email
    # profile_id = verify_email(user["code"])
    # if not profile_id:
    #     continue  # Skip to next user if verification fails

    # Step 2: Add Basic Info
    add_basic_info(user["profile_id"], user["fname"], user["lname"], user["tuftsid"])

    # Step 3: Upload Profile Photo
    upload_profile_photo(user["profile_id"], user["profile_photo"])

    # Step 4: Add Interests
    add_interests(user["profile_id"], user["interests"])

    # Step 5: Add Offerings
    add_offerings(user["profile_id"], user["offerings"])

print("\n✅ All users processed successfully!")