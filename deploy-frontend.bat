@echo off
cd "c:\Finance Expense Tracker\frontend"
echo Building frontend...
gcloud builds submit --tag us-central1-docker.pkg.dev/finance-expenses-app/expense-tracker-repo/expense-tracker-frontend
echo Deploying frontend...
gcloud run deploy expense-tracker-frontend --image us-central1-docker.pkg.dev/finance-expenses-app/expense-tracker-repo/expense-tracker-frontend --platform managed --region us-central1 --allow-unauthenticated
echo Frontend deployment complete!