#!/bin/bash

echo "🚀 DEPLOYING FOOD BOT BACKEND TO GOOGLE CLOUD RUN"
echo "=================================================="

gcloud run deploy food-bot-backend \
  --source . \
  --region asia-south1 \
  --allow-unauthenticated \
  --memory=2Gi \
  --cpu=2 \
  --timeout=1000 \
  --service-account=firebase-adminsdk-c8acd@chat-app-f3937.iam.gserviceaccount.com \
  --set-env-vars="GOOGLE_CLOUD_PROJECT=chat-app-f3937,GEMINI_API_KEY=AIzaSyDFbQKMuj3brfwz1hDgKksHZeg1gScNYxw" \
  --port=5003

echo ""
echo "🎉 DEPLOYMENT COMPLETE!"
echo "🌐 Your API is available at: https://food-bot-backend-wiyrvumxlq-el.a.run.app"
