#!/bin/bash

# Setup and Deploy Food Bot Backend to Cloud Run
# This script sets up the service account and deploys the application

set -e  # Exit on any error

PROJECT_ID="chat-app-f3937"
SERVICE_NAME="food-bot-backend"
REGION="asia-south1"
SERVICE_ACCOUNT_NAME="food-bot-sa"

echo "🚀 Setting up and deploying Food Bot Backend..."
echo "📋 Project ID: $PROJECT_ID"
echo "🌍 Region: $REGION"

# Set the project
echo "🔧 Setting project..."
gcloud config set project $PROJECT_ID

# Create service account if it doesn't exist
echo "👤 Creating service account..."
if ! gcloud iam service-accounts describe $SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com &>/dev/null; then
    gcloud iam service-accounts create $SERVICE_ACCOUNT_NAME \
        --display-name="Food Bot Service Account" \
        --description="Service account for food bot backend"
    echo "✅ Service account created"
else
    echo "ℹ️  Service account already exists"
fi

# Grant Firestore permissions
echo "🔐 Granting Firestore permissions..."
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/datastore.user"

echo "✅ Permissions granted"

# Deploy the application
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --source . \
    --region $REGION \
    --platform managed \
    --allow-unauthenticated \
    --memory=2Gi \
    --cpu=2 \
    --timeout=1000 \
    --concurrency=10 \
    --max-instances=10 \
    --service-account=$SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com

echo "🎉 Deployment completed successfully!"
echo "🌐 Your app should be available at the URL shown above"
