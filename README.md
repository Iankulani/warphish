# warphish

<img width="1106" height="824" alt="war phish" src="https://github.com/user-attachments/assets/172e77f4-d2f3-417d-bfe6-01012d68129f" />

[![GitHub stars](https://img.shields.io/github/stars/Iankulani/warphish?style=for-the-badge&logo=github)](https://github.com/Iankulani/warphish/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Iankulani/warphish?style=for-the-badge&logo=github)](https://github.com/Iankulani/warphish/network)
[![GitHub watchers](https://img.shields.io/github/watchers/Iankulani/warphish?style=for-the-badge&logo=github)](https://github.com/Iankulani/warphish/watchers)
[![GitHub contributors](https://img.shields.io/github/contributors/Iankulani/warphish?style=for-the-badge&logo=github)](https://github.com/Iankulani/warphish/graphs/contributors)
[![GitHub last commit](https://img.shields.io/github/last-commit/Iankulani/warphish?style=for-the-badge&logo=git)](https://github.com/Iankulani/warphish/commits/main)
[![Docker Pulls](https://img.shields.io/docker/pulls/iankulaniking_phisher/warphish?style=for-the-badge&logo=docker&logoColor=white)](https://hub.docker.com/r/iankulaniking_phisher/warphish) <!-- Replace with actual Docker Hub path if different -->
[![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20%7C%20macOS-blue?style=for-the-badge&logo=linux&logoColor=white)](https://github.com/Iankulani/warphish)
[![Python](https://img.shields.io/badge/python-3.x-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

War Phish is an advanced cybersecurity operations platform engineered to unify offensive security testing, social engineering simulations, remote command orchestration, and network intelligence into a single command-driven ecosystem. Designed for security researchers, red teams, penetration testers, cyber defense analysts, and enterprise security operators, the platform provides a powerful framework for conducting controlled security assessments, awareness campaigns, and tactical infrastructure operations across multiple communication environments and deployment channels.

# Clone repository
```bash
git clone https://github.com/Iankulani/warphish.git

cd warphish
```

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
