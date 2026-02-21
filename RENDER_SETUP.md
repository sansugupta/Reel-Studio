# Render.com Deployment (100% Free Forever!)

## Why Render?
- Completely free tier (no credit card!)
- 750 hours/month free
- Auto-deploys from GitHub
- No payment verification needed

## Step 1: Create Render Account
1. Go to https://render.com
2. Sign up with GitHub (no card needed!)
3. Authorize Render

## Step 2: Deploy Backend

1. Click "New +" → "Web Service"
2. Connect your GitHub: `sansugupta/Reel-Studio`
3. Configure:
   - Name: `reel-studio-backend`
   - Region: Oregon (US West)
   - Branch: `main`
   - Root Directory: `backend`
   - Runtime: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Instance Type: `Free`

4. Add Environment Variables:
   ```
   ADMIN_TOKEN=your-secret-token
   MAX_FILE_SIZE=209715200
   CLEANUP_INTERVAL_MINUTES=5
   FILE_MAX_AGE_MINUTES=30
   PYTHON_VERSION=3.11.0
   ```

5. Click "Create Web Service"

## Step 3: Deploy Frontend

1. Click "New +" → "Static Site"
2. Connect same repo: `sansugupta/Reel-Studio`
3. Configure:
   - Name: `reel-studio-frontend`
   - Branch: `main`
   - Root Directory: `frontend`
   - Build Command: `npm install && npm run build`
   - Publish Directory: `.next`

4. Add Environment Variable:
   ```
   NEXT_PUBLIC_API_URL=https://reel-studio-backend.onrender.com
   ```
   (Use your backend URL from step 2)

5. Click "Create Static Site"

## Step 4: Access Your App

Your app will be live at:
- Frontend: `https://reel-studio-frontend.onrender.com`
- Backend: `https://reel-studio-backend.onrender.com`
- Admin: `https://reel-studio-frontend.onrender.com/admin`

## Important Notes

### Cold Starts
- Free tier spins down after 15 minutes of inactivity
- First request takes ~30-60 seconds to wake up
- Subsequent requests are fast

### Limitations
- 512MB RAM (can handle 1-2 concurrent videos)
- Slower than paid options
- Cold start delay

### Keep It Awake (Optional)
Use a free service like UptimeRobot to ping your app every 14 minutes:
1. Go to https://uptimerobot.com
2. Add monitor for your Render URL
3. Check every 5 minutes

## Managing Your App

### View Logs
Go to Render dashboard → Your service → Logs

### Redeploy
```bash
git push origin main
# Render auto-deploys
```

### Manual Deploy
Render dashboard → Your service → "Manual Deploy"

## Cost
**$0/month forever!** (with limitations above)

## Performance
- Good for personal use or demos
- 1-2 concurrent users
- Video processing: ~40-60 seconds
- Perfect for sharing with friends

## Upgrade Path
If you need better performance later:
- Render Starter: $7/month (no cold starts, more RAM)
- Railway: $5 credit/month
- Oracle Cloud: Free tier with card verification
