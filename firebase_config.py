import os
import logging
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud import firestore as gcp_firestore
from google.api_core.exceptions import GoogleAPIError
import time

# Reduce noisy logs and set timeouts
os.environ.setdefault("GRPC_VERBOSITY", "ERROR")
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", "chat-app-f3937")
logging.getLogger('grpc').setLevel(logging.ERROR)
logging.getLogger('google.auth.transport.grpc').setLevel(logging.ERROR)
logging.getLogger('google.auth').setLevel(logging.ERROR)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class FirebaseConfig:
    def __init__(self, key_path: str = "./firebase.json", project_id: str = None):
        self.db = None
        self.key_path = os.path.abspath(key_path) if key_path else None
        # Prefer explicit project id, else env set by Cloud Run
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT", "chat-app-f3937")
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
                    database='(default)'
                )
                print("✅ FIREBASE CONFIG: Firebase already initialized, using existing client for '(default)' database")
                return
            else:
                print("📭 FIREBASE CONFIG: No existing Firebase apps found, initializing new one")
            
            # Initialize Firebase credentials with fallbacks
            # Priority:
            # 1) GOOGLE_APPLICATION_CREDENTIALS
            # 2) FIREBASE_KEY_FILE env
            # 3) firebase.json in current directory
            # 4) Application Default Credentials (last resort)
            gac_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
            key_file_path = os.getenv('FIREBASE_KEY_FILE')
            local_key_path = './firebase.json'
            
            print(f"🔍 FIREBASE CONFIG: GOOGLE_APPLICATION_CREDENTIALS: {gac_path}")
            if key_file_path:
                print(f"🔍 FIREBASE CONFIG: FIREBASE_KEY_FILE: {key_file_path}")
                print(f"📂 FIREBASE CONFIG: Absolute path: {os.path.abspath(key_file_path)}")

            cred_obj = None
            if gac_path and os.path.exists(gac_path):
                print("📁 FIREBASE CONFIG: Using GOOGLE_APPLICATION_CREDENTIALS for credentials")
                cred_obj = credentials.Certificate(gac_path)
            elif key_file_path and os.path.exists(key_file_path):
                print("📁 FIREBASE CONFIG: Using FIREBASE_KEY_FILE for credentials")
                cred_obj = credentials.Certificate(key_file_path)
            elif os.path.exists(local_key_path):
                print("📁 FIREBASE CONFIG: Using local firebase.json for credentials")
                cred_obj = credentials.Certificate(local_key_path)
            else:
                print("ℹ️  FIREBASE CONFIG: No key files present. Using Application Default Credentials")
                try:
                    firebase_admin.initialize_app()
                    print("✅ FIREBASE CONFIG: Firebase app initialized with ADC")
                except Exception as adc_err:
                    print(f"❌ FIREBASE CONFIG: ADC initialization failed: {adc_err}")
                    print(f"📂 FIREBASE CONFIG: Directory contents: {os.listdir('.')}")
                    raise

            if cred_obj is not None:
                print("🚀 FIREBASE CONFIG: Initializing Firebase app with explicit credentials...")
                firebase_admin.initialize_app(cred_obj)
                print("✅ FIREBASE CONFIG: Firebase app initialized with explicit credentials")
            
            print(f"📊 FIREBASE CONFIG: Firebase apps count: {len(firebase_admin._apps)}")
            
            # Create Firestore client with specific database
            print("🔗 FIREBASE CONFIG: Getting Firestore client for '(default)' database...")
            # Get the credentials from the Firebase app
            app = firebase_admin.get_app()
            try:
                cred = app.credential.get_credential()
                self.db = gcp_firestore.Client(
                    project=self.project_id,
                    credentials=cred,
                    database='(default)'
                )
            except Exception:
                print("ℹ️  FIREBASE CONFIG: Falling back to Firestore Client with ADC")
                self.db = gcp_firestore.Client(
                    project=self.project_id,
                    database='(default)'
                )
            print("✅ FIREBASE CONFIG: Firestore client created successfully")
            print(f"🔗 FIREBASE CONFIG: Firestore client type: {type(self.db)}")
            print(f"📊 FIREBASE CONFIG: Using database: (default)")
            
            # Skip connectivity test to avoid hanging
            print("⚠️  FIREBASE CONFIG: Skipping connectivity test to avoid hanging")
            print("✅ FIREBASE CONFIG: Firebase initialized successfully")
            print(f"📊 FIREBASE CONFIG: Database: (default) (Firestore)")
            
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
