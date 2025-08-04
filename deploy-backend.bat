@echo off
echo Deploying Finance Expense Tracker Backend...
cd "c:\Finance Expense Tracker\backend"

echo Building backend image...
gcloud builds submit --tag us-central1-docker.pkg.dev/finance-expenses-app/cloud-run-source-deploy/finance-expense-tracker-backend

echo Deploying backend to Cloud Run...
gcloud run deploy finance-expense-tracker --image us-central1-docker.pkg.dev/finance-expenses-app/cloud-run-source-deploy/finance-expense-tracker-backend --platform managed --region us-central1 --allow-unauthenticated --add-cloudsql-instances=finance-expenses-app:us-central1:expense-tracker-db

echo Backend deployment complete!
echo Service URL: https://finance-expense-tracker-467666307950.us-central1.run.app