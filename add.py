import firebase_admin
from firebase_admin import credentials, firestore
import logging

logging.getLogger('google.auth').setLevel(logging.ERROR)

# Path to your service account key
cred = credentials.Certificate("./firebase.json")
print("✅ Credentials loaded successfully 1")
# Initialize the Firebase app
firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()
print("✅ Credentials loaded successfully 2")

# Example: add a document to a collection
data = {
    "name": "Kavleen",
    "role": "Engineer",
    "created_at": firestore.SERVER_TIMESTAMP
}
print("✅ Credentials loaded successfully 3")


# Add to collection "users"
try:
    doc_ref = db.collection("users").add(data)
    print("✅ Data added successfully:", doc_ref)
except Exception as e:
    print("❌ Error adding data:", e)
print("✅ Data added successfully:")
