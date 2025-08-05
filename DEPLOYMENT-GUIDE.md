# 🚀 Finance Expense Tracker - Production Setup Guide

## ✅ What's Been Updated

Your project has been configured for production deployment with these key changes:

### File Structure Updates
- ✅ **Dockerfile moved to backend/** - Now correctly builds from backend context
- ✅ **Frontend Dockerfile** - Updated for Cloud Run port 8080
- ✅ **cloudbuild.yaml** - Complete CI/CD pipeline for both frontend and backend
- ✅ **Deployment scripts** - Updated with correct service names and image paths
- ✅ **README.md** - Comprehensive documentation

### Service Name Changes
- ✅ **Backend service**: `finance-expense-tracker`
- ✅ **Frontend service**: `finance-expense-tracker-frontend`
- ✅ **Image names**: More meaningful names in `cloud-run-source-deploy` repository

### Environment Configuration
- ✅ **Local development**: Uses `.env` file with SQLite
- ✅ **Production**: Uses Cloud Run environment variables with Cloud SQL
- ✅ **Template created**: `.env.production.template` for reference

---

## 🔧 Next Steps for Production Deployment

### 1. Set Environment Variables in Cloud Run

You MUST set these environment variables in the Cloud Run console:

```bash
# Go to Cloud Run → finance-expense-tracker → Edit & Deploy New Revision → Environment Variables
SECRET_KEY=key
JWT_SECRET_KEY=key
HUGGING_FACE_TOKEN=key
DB_PASS=key
```

The following are already set via cloudbuild.yaml:
- `DB_USER=postgres`
- `DB_NAME=expense_tracker`
- `CLOUD_SQL_CONNECTION_NAME=finance-expenses-app:us-central1:expense-tracker-db`

### 2. Deploy Using Cloud Build Trigger

Your project is set up for automatic deployment:

1. **Commit and push your changes**:
   ```bash
   git add .
   git commit -m "Production deployment configuration"
   git push origin main
   ```

2. **Monitor the build** in Cloud Build console
3. **Check deployment** in Cloud Run console

### 3. Manual Deployment (Alternative)

If you prefer manual deployment:

```bash
# Backend only
.\deploy-backend.bat

# Frontend only
.\deploy-frontend.bat
```

### 4. Local Development

For local development:

```bash
# Start both services
.\start-local-dev.bat

# Or manually:
# Backend: cd backend && python app.py
# Frontend: cd frontend && npm start
```

---

## 🎯 Expected URLs After Deployment

- **Backend API**: https://finance-expense-tracker-467666307950.us-central1.run.app
- **Frontend App**: https://finance-expense-tracker-frontend-[YOUR-HASH].us-central1.run.app

---

## ⚠️ Important Security Notes

1. **Never commit secrets** to Git - they're already in `.gitignore`
2. **Set environment variables** only in Cloud Run console for production
3. **Use different keys** for production vs development
4. **Rotate keys periodically**

---

## 🐛 Common Issues & Solutions

### Build Fails with "requirements.txt not found"
- ✅ **Fixed**: Dockerfile now in `backend/` folder with correct context

### Environment Variables Not Working
- ⚠️ **Action Required**: Set them manually in Cloud Run console (see step 1 above)

### AI Categorization Not Working
- ⚠️ **Action Required**: Ensure `HUGGING_FACE_TOKEN` is set in Cloud Run

### Frontend Can't Connect to Backend
- ✅ **Fixed**: Frontend API URL updated to production backend URL

---

## 📋 Deployment Checklist

- [ ] Set environment variables in Cloud Run console
- [ ] Push code to trigger automatic build
- [ ] Verify backend deployment at API URL
- [ ] Verify frontend deployment works
- [ ] Test user registration/login
- [ ] Test expense creation and AI categorization
- [ ] Test dashboard and analytics

---

## 🚀 You're Ready!

Your project is now configured for production deployment. Follow the steps above and you'll have a fully functional expense tracker running on Google Cloud!

Need help? Check the main README.md for detailed documentation and troubleshooting.
