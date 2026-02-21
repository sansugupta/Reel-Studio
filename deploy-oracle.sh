#!/bin/bash

# Oracle Cloud Deployment Script for Reel-Studio
# Run this on your Oracle Cloud VM

echo "🚀 Deploying Reel-Studio on Oracle Cloud..."

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.11
sudo apt install -y software-properties-common
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3.11-dev

# Install FFmpeg
sudo apt install -y ffmpeg

# Install Node.js 18
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Install Nginx
sudo apt install -y nginx

# Install PM2 for process management
sudo npm install -g pm2

# Clone repository (if not already cloned)
if [ ! -d "Reel-Studio" ]; then
    git clone https://github.com/sansugupta/Reel-Studio.git
fi

cd Reel-Studio

# Setup Backend
cd backend
python3.11 -m venv venv311
source venv311/bin/activate
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
ADMIN_TOKEN=$(openssl rand -hex 32)
MAX_FILE_SIZE=209715200
CLEANUP_INTERVAL_MINUTES=5
FILE_MAX_AGE_MINUTES=30
EOF

echo "Admin Token: $(grep ADMIN_TOKEN .env | cut -d'=' -f2)"

# Start backend with PM2
pm2 start "source venv311/bin/activate && uvicorn main:app --host 0.0.0.0 --port 8000" --name reel-studio-backend

cd ../frontend

# Setup Frontend
npm install
npm run build

# Create production env
cat > .env.production << EOF
NEXT_PUBLIC_API_URL=http://$(curl -s ifconfig.me):8000
EOF

# Start frontend with PM2
pm2 start npm --name reel-studio-frontend -- start

# Save PM2 configuration
pm2 save
pm2 startup

# Configure Nginx
sudo tee /etc/nginx/sites-available/reel-studio << EOF
server {
    listen 80;
    server_name _;

    client_max_body_size 200M;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }

    location /outputs {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/reel-studio /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl restart nginx

# Configure firewall
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 443 -j ACCEPT
sudo netfilter-persistent save

echo "✅ Deployment complete!"
echo "🌐 Access your app at: http://$(curl -s ifconfig.me)"
echo "🔑 Admin Token saved in backend/.env"
echo ""
echo "Useful commands:"
echo "  pm2 status          - Check app status"
echo "  pm2 logs            - View logs"
echo "  pm2 restart all     - Restart services"
