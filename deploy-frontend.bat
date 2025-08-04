@echo off
echo Deploying Finance Expense Tracker Frontend...
cd "c:\Finance Expense Tracker\frontend"

echo Building frontend image...
gcloud builds submit --tag us-central1-docker.pkg.dev/finance-expenses-app/cloud-run-source-deploy/finance-expense-tracker-frontend

echo Deploying frontend to Cloud Run...
gcloud run deploy finance-expense-tracker-frontend --image us-central1-docker.pkg.dev/finance-expenses-app/cloud-run-source-deploy/finance-expense-tracker-frontend --platform managed --region us-central1 --allow-unauthenticated --port=8080

echo Frontend deployment complete!
echo Frontend URL: https://finance-expense-tracker-frontend-467666307950.us-central1.run.app