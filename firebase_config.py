import os
import logging
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud import firestore as gcp_firestore
from google.api_core.exceptions import GoogleAPIError
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get configuration from environment variables with defaults
FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID", "food-recommend-39842")
FIREBASE_DATABASE_ID = os.getenv("FIREBASE_DATABASE_ID", "food-bot")
FIREBASE_KEY_FILE = os.getenv("FIREBASE_KEY_FILE", "firebase.json")

# Reduce noisy logs and set timeouts
os.environ.setdefault("GRPC_VERBOSITY", "ERROR")
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", FIREBASE_PROJECT_ID)
logging.getLogger('grpc').setLevel(logging.ERROR)
logging.getLogger('google.auth.transport.grpc').setLevel(logging.ERROR)
logging.getLogger('google.auth').setLevel(logging.ERROR)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class FirebaseConfig:
    def __init__(self, key_path: str = None, project_id: str = None, database_id: str = None):
        self.db = None
        self.key_path = os.path.abspath(key_path) if key_path else FIREBASE_KEY_FILE
        self.project_id = project_id or FIREBASE_PROJECT_ID
        self.database_id = database_id or FIREBASE_DATABASE_ID
        self._initialize_firebase()

    def _initialize_firebase(self):
        print("🔥 FIREBASE CONFIG: Starting Firebase initialization...")
        print(f"📅 FIREBASE CONFIG: Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📂 FIREBASE CONFIG: Current working directory: {os.getcwd()}")
        
        try:
            # Check if Firebase is already initialized
            print("🔍 FIREBASE CONFIG: Checking if Firebase is already initialized...")
            if firebase_admin._apps:
                print(f"📊 FIREBASE CONFIG: Found {len(firebase_admin._apps)} existing Firebase apps")
                app = firebase_admin.get_app()
                cred = app.credential.get_credential()
                self.db = gcp_firestore.Client(
                    project=self.project_id,
                    credentials=cred,
                    database=self.database_id
                )
                print(f"✅ FIREBASE CONFIG: Firebase already initialized, using existing client for '{self.database_id}' database")
                return
            else:
                print("📭 FIREBASE CONFIG: No existing Firebase apps found, initializing new one")
            
            # Initialize Firebase with service account key
            key_file_path = self.key_path
            print(f"🔍 FIREBASE CONFIG: Looking for key file at: {key_file_path}")
            print(f"📂 FIREBASE CONFIG: Absolute path: {os.path.abspath(key_file_path)}")
            
            if os.path.exists(key_file_path):
                print("📁 FIREBASE CONFIG: Key file found")
                print("🔧 FIREBASE CONFIG: Creating credentials object...")
                cred = credentials.Certificate(key_file_path)
                print("✅ FIREBASE CONFIG: Credentials object created successfully")
                
                print("🚀 FIREBASE CONFIG: Initializing Firebase app...")
                firebase_admin.initialize_app(cred)
                print("✅ FIREBASE CONFIG: Firebase app initialized with key file")
                print(f"📊 FIREBASE CONFIG: Firebase apps count: {len(firebase_admin._apps)}")
            else:
                print("❌ FIREBASE CONFIG: Key file not found")
                print(f"📂 FIREBASE CONFIG: Directory contents: {os.listdir('.')}")
                raise ValueError(f"{key_file_path} not found")
            
            # Create Firestore client with specific database
            print(f"🔗 FIREBASE CONFIG: Getting Firestore client for '{self.database_id}' database...")
            # Get the credentials from the Firebase app
            app = firebase_admin.get_app()
            cred = app.credential.get_credential()
            self.db = gcp_firestore.Client(
                project=self.project_id,
                credentials=cred,
                database=self.database_id
            )
            print("✅ FIREBASE CONFIG: Firestore client created successfully")
            print(f"🔗 FIREBASE CONFIG: Firestore client type: {type(self.db)}")
            print(f"📊 FIREBASE CONFIG: Using database: {self.database_id}")
            
            # Skip connectivity test to avoid hanging
            print("⚠️  FIREBASE CONFIG: Skipping connectivity test to avoid hanging")
            print("✅ FIREBASE CONFIG: Firebase initialized successfully")
            print(f"📊 FIREBASE CONFIG: Database: {self.database_id} (Firestore)")
            
        except Exception as e:
            print(f"❌ FIREBASE CONFIG: Firebase initialization failed: {e}")
            print(f"❌ FIREBASE CONFIG: Error type: {type(e).__name__}")
            print("Please check your Firebase configuration")
            import traceback
            print("📋 FIREBASE CONFIG: Full traceback:")
            traceback.print_exc()
            raise e

    def get_db(self):
        print("🔍 FIREBASE CONFIG: get_db() called")
        if not self.db:
            print("🔄 FIREBASE CONFIG: Database not initialized, calling _initialize_firebase()")
            self._initialize_firebase()
        else:
            print("✅ FIREBASE CONFIG: Database already initialized, returning existing client")
        print(f"📊 FIREBASE CONFIG: Returning database client: {type(self.db)}")
        return self.db
    

# Example global instance (be mindful in serverless cold starts)
firebase_config = FirebaseConfig()
