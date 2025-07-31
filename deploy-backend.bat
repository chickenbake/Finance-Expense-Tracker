@echo off
cd "c:\Finance Expense Tracker\backend"
echo Building backend...
gcloud builds submit --tag us-central1-docker.pkg.dev/finance-expenses-app/expense-tracker-repo/expense-tracker-backend
echo Deploying backend...
gcloud run deploy expense-tracker-backend --image us-central1-docker.pkg.dev/finance-expenses-app/expense-tracker-repo/expense-tracker-backend --platform managed --region us-central1 --allow-unauthenticated
echo Backend deployment complete!