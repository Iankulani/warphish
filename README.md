# warphish

<img width="1536" height="1024" alt="war phish" src="https://github.com/user-attachments/assets/922c0af7-fd0a-4f16-b5f5-7600c4aa5988" />

warphish


# Clone repository
git clone https://github.com/Iankulani/warphish.git
cd warphish

# Run installer
setup.bat

# Activate environment
venv\Scripts\activate

# Run WAR PHISH
python warphish.py
Docker
bash
# Build image
docker build -t warphish:latest .

# Run with docker-compose
docker-compose up -d

# Or run directly
```bash
docker run -it --rm --privileged --network host warphish:latest
```
# System Dependencies
# Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install -y \
    nmap hping3 dsniff macchanger tcpdump \
    netcat-openbsd whois dnsutils curl wget ssh \
    python3-pip build-essential libpcap-dev
RHEL/CentOS/Fedora
sudo yum install -y \
    nmap hping3 dsniff macchanger tcpdump \
    nc whois bind-utils curl wget openssh-clients \
    python3-devel libpcap-devel
```
# macOS
```bash
brew install nmap hping3 dsniff macchanger tcpdump netcat whois curl wget
# Bot Configuration
# Discord Bot
Go to https://discord.com/developers/applications

Create new application → Bot

Copy token to .env as DISCORD_TOKEN

Enable Privileged Gateway Intents

Telegram Bot
Message @BotFather on Telegram

Create new bot with /newbot

Copy token to .env as TELEGRAM_BOT_TOKEN

Get API ID/Hash from https://my.telegram.org

Slack Bot
Go to https://api.slack.com/apps

Create new app → From scratch

Add Bot Token scope

Install to workspace → Copy token

Running as Root
For full functionality (packet capture, spoofing), run as root:

```bash
sudo python3 warphish.py
```
# or
```bash
sudo docker-compose up -d
```
Troubleshooting
Common Issues

"Module not found"

```bash
pip install -r requirements.txt --force-reinstall
"Permission denied" (Linux)
```
```bash
sudo chmod +x warphish.py
sudo ./warphish.py
"Address already in use"
```

# Change ports in config or kill existing processes
```bash
sudo lsof -i :5000
sudo kill -9 <PID>
Docker issues
```

# Rebuild
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
Post-Installation
Edit .env with your bot tokens

Configure web dashboard settings

Test with ping 127.0.0.1

Generate test phishing link

Access dashboard at http://localhost:5000
```
Updating

```bash
git pull
source venv/bin/activate
pip install -r requirements.txt --upgrade
python3 warphish.py
```
