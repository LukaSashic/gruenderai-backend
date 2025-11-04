# GründerAI Backend - Railway Deployment Guide

## 📦 What's Included

This backend provides the API for the GründerAI assessment system:
- FastAPI application with CORS support
- 15-question assessment covering 5 dimensions
- Sophisticated scoring and analysis engine
- Session management
- Results calculation with personalized recommendations

## 🚀 Deploy to Railway (Recommended)

### Prerequisites
- GitHub account
- Railway account (sign up at railway.app)

### Step 1: Prepare Repository

```bash
# Create a new GitHub repository
# Repository name: gruenderai-backend

# Clone locally
git clone https://github.com/YOUR_USERNAME/gruenderai-backend.git
cd gruenderai-backend

# Copy all backend files to this directory:
# - main.py
# - requirements.txt
# - Procfile
# - assessment/ folder (with __init__.py, engine.py, questions.py)

# Initialize git and push
git add .
git commit -m "Initial backend setup"
git push origin main
```

### Step 2: Deploy on Railway

1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Authorize Railway to access your GitHub
5. Select your `gruenderai-backend` repository
6. Railway will automatically detect Python and start deploying

### Step 3: Configure Environment (if needed)

Railway should auto-detect everything, but verify:
- Build Command: (auto-detected from requirements.txt)
- Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Step 4: Get Your API URL

Once deployed, Railway will provide a URL like:
```
https://gruenderai-backend-production.up.railway.app
```

**IMPORTANT:** Copy this URL - you'll need it for the frontend!

### Step 5: Test Your API

Test the health endpoint:
```bash
curl https://YOUR_RAILWAY_URL.railway.app/health
```

You should see:
```json
{
  "status": "healthy",
  "active_sessions": 0,
  "timestamp": "..."
}
```

## 🔧 Alternative: Manual Deployment

If you prefer to deploy manually:

### Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python main.py

# Test at http://localhost:8000
```

### Deploy to Other Platforms

The app is compatible with:
- **Render**: Similar to Railway
- **Fly.io**: Great for global distribution
- **Google Cloud Run**: Serverless option
- **AWS Elastic Beanstalk**: Enterprise option

## 📝 Environment Variables

Currently, no environment variables are required for basic operation.

For production, you may want to add:
- `DATABASE_URL`: PostgreSQL connection string (for persistent storage)
- `REDIS_URL`: Redis URL (for session management)
- `CORS_ORIGINS`: Specific domains allowed

## 🐛 Troubleshooting

### Deployment fails
- Check Railway logs for errors
- Verify all files are committed and pushed
- Ensure requirements.txt is in root directory

### CORS errors from frontend
- Verify your frontend domain is in the CORS allowed origins in main.py
- Add your custom domain after deployment

### API returns 404
- Ensure URL ends with /api/assessment/start (not just base URL)
- Check Railway logs for routing issues

## 📊 Monitoring

Railway provides:
- Automatic logs
- Metrics dashboard
- Deployment history
- Easy rollback

Access these in your Railway dashboard.

## 💰 Pricing

Railway offers:
- Free tier: $5 credit/month (enough for testing)
- Pay-as-you-go: ~$0.000463/GB-second
- Estimated cost: $5-20/month for moderate traffic

## 🔄 Updates

To deploy updates:

```bash
# Make changes to your code
git add .
git commit -m "Your update message"
git push origin main

# Railway auto-deploys on push!
```

## ✅ Deployment Checklist

- [ ] Create GitHub repository
- [ ] Push backend files
- [ ] Deploy to Railway
- [ ] Copy API URL
- [ ] Test health endpoint
- [ ] Update frontend with API URL
- [ ] Test end-to-end flow

## 🆘 Support

If you run into issues:
1. Check Railway logs
2. Verify file structure matches this guide
3. Test API endpoints with curl/Postman
4. Check CORS configuration

---

**Next Step:** Deploy the frontend to Vercel using the frontend README!
