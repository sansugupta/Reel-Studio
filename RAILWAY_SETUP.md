# Railway Deployment Guide (No Credit Card Required!)

## Why Railway?
- No credit card needed for trial
- $5 free credit monthly (enough for moderate usage)
- Auto-deploys from GitHub
- Supports AI workloads (Demucs)
- Easy setup

## Step 1: Create Railway Account
1. Go to https://railway.app
2. Sign up with GitHub (no credit card needed)
3. Authorize Railway to access your repos

## Step 2: Deploy Reel-Studio

### Option A: One-Click Deploy (Easiest)
1. Go to your Railway dashboard
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose `sansugupta/Reel-Studio`
5. Railway will auto-detect and deploy

### Option B: Railway CLI
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link to your repo
cd Reel-Studio
railway link

# Deploy
railway up
```

## Step 3: Configure Environment Variables

In Railway dashboard, add these variables:
```
ADMIN_TOKEN=your-secret-token-here
MAX_FILE_SIZE=209715200
CLEANUP_INTERVAL_MINUTES=5
FILE_MAX_AGE_MINUTES=30
```

## Step 4: Get Your URL

Railway will provide a public URL like:
`https://reel-studio-production.up.railway.app`

Access your app at that URL!

## Managing Your App

### View Logs
```bash
railway logs
```

### Redeploy
```bash
git push origin main
# Railway auto-deploys on push
```

### Check Status
Go to Railway dashboard to see:
- Deployment status
- Resource usage
- Logs
- Metrics

## Cost Estimate
- Free tier: $5 credit/month
- Typical usage: ~$3-4/month for light traffic
- First month completely free

## Performance Notes
- Railway provides 512MB-1GB RAM
- Good for 2-3 concurrent video processing
- Cold starts: ~10-15 seconds
- Processing time: ~30-40 seconds per video

## Limitations
- Smaller than Oracle Cloud (but no card needed!)
- May need to upgrade for heavy traffic
- Files auto-delete after 30 minutes (as designed)

## Alternative: Render.com

If Railway doesn't work, try Render:

1. Go to https://render.com
2. Sign up (no card needed)
3. New Web Service → Connect GitHub
4. Select Reel-Studio repo
5. Configure:
   - Build: `cd backend && pip install -r requirements.txt`
   - Start: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`

Render is slower but completely free forever (750 hours/month).
