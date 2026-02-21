# Oracle Cloud Free Tier Deployment Guide

## Why Oracle Cloud?
- **4 ARM CPUs + 24GB RAM** (Always Free!)
- **200GB storage**
- **10TB bandwidth/month**
- Perfect for AI workloads like Demucs

## Step 1: Create Oracle Cloud Account
1. Go to https://www.oracle.com/cloud/free/
2. Sign up for Always Free tier
3. Verify your account

## Step 2: Create a VM Instance

1. Go to **Compute** → **Instances** → **Create Instance**

2. Configure:
   - **Name**: reel-studio
   - **Image**: Ubuntu 22.04 (Canonical)
   - **Shape**: VM.Standard.A1.Flex (ARM)
     - OCPUs: 4
     - Memory: 24 GB
   - **Boot Volume**: 200 GB

3. **Networking**:
   - Create new VCN or use existing
   - Assign public IP
   - Download SSH keys

4. Click **Create**

## Step 3: Configure Security Rules

1. Go to **Networking** → **Virtual Cloud Networks**
2. Click your VCN → **Security Lists** → **Default Security List**
3. Add Ingress Rules:
   - **Port 80** (HTTP): Source 0.0.0.0/0
   - **Port 443** (HTTPS): Source 0.0.0.0/0
   - **Port 22** (SSH): Source 0.0.0.0/0

## Step 4: Connect to Your VM

```bash
chmod 400 your-ssh-key.pem
ssh -i your-ssh-key.pem ubuntu@YOUR_PUBLIC_IP
```

## Step 5: Deploy Reel-Studio

```bash
# Download deployment script
wget https://raw.githubusercontent.com/sansugupta/Reel-Studio/main/deploy-oracle.sh

# Make it executable
chmod +x deploy-oracle.sh

# Run deployment
./deploy-oracle.sh
```

The script will:
- Install all dependencies (Python 3.11, Node.js, FFmpeg, Nginx)
- Setup backend and frontend
- Configure Nginx reverse proxy
- Start services with PM2
- Generate admin token

## Step 6: Access Your App

After deployment completes:
- **App URL**: http://YOUR_PUBLIC_IP
- **Admin Dashboard**: http://YOUR_PUBLIC_IP/admin
- **Admin Token**: Check `backend/.env` file

## Managing Your App

### View Status
```bash
pm2 status
```

### View Logs
```bash
pm2 logs reel-studio-backend
pm2 logs reel-studio-frontend
```

### Restart Services
```bash
pm2 restart all
```

### Stop Services
```bash
pm2 stop all
```

### Update Code
```bash
cd Reel-Studio
git pull
pm2 restart all
```

## Optional: Setup Domain & SSL

### 1. Point Domain to Your IP
Add an A record pointing to your Oracle Cloud IP

### 2. Install Certbot
```bash
sudo apt install -y certbot python3-certbot-nginx
```

### 3. Get SSL Certificate
```bash
sudo certbot --nginx -d yourdomain.com
```

### 4. Auto-renewal
```bash
sudo certbot renew --dry-run
```

## Monitoring

### Check Disk Space
```bash
df -h
```

### Check Memory
```bash
free -h
```

### Check CPU
```bash
htop
```

### Check Nginx
```bash
sudo systemctl status nginx
```

## Troubleshooting

### Port 80 not accessible?
```bash
# Check Oracle Cloud security list (Step 3)
# Check VM firewall
sudo iptables -L -n
```

### Services not starting?
```bash
pm2 logs
# Check for errors
```

### Out of memory?
```bash
# Check processing jobs
pm2 monit
# Restart if needed
pm2 restart all
```

## Cost Estimate
**$0/month** - Everything runs on Always Free tier!

## Performance
- Can handle 5-10 concurrent video processing jobs
- Each 30-second video processes in ~20-30 seconds
- Demucs AI runs smoothly on ARM CPUs
