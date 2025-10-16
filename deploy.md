# Deploy to Cloud Run

# First, set up the service account with proper permissions
gcloud iam service-accounts create food-bot-sa \
  --display-name="Food Bot Service Account" \
  --description="Service account for food bot backend"

# Grant Firestore permissions
gcloud projects add-iam-policy-binding chat-app-f3937 \
  --member="serviceAccount:food-bot-sa@chat-app-f3937.iam.gserviceaccount.com" \
  --role="roles/datastore.user"

# Deploy the application
gcloud run deploy food-bot-backend \
  --source . \
  --region asia-south1 \
  --platform managed \
  --allow-unauthenticated \
  --memory=2Gi \
  --cpu=2 \
  --timeout=1000 \
  --concurrency=10 \
  --max-instances=10 \
  --service-account=food-bot-sa@chat-app-f3937.iam.gserviceaccount.com 
