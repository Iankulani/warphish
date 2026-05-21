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

War Phish is an all-in-one adversarial emulation software designed for red team operators, white hat hackers, and authorized security professionals. Built by Accurate Cyber Defense, it merges social engineering, network exploitation, and real-time C2 communication into a single attack framework. War Phish is also embraced by red hat hackers for proactive threat hunting and counter-adversary operations.

Key Capabilities

Cyber Drill Simulations
Launch full-scope breach exercises: phishing campaigns, credential harvesting, endpoint deployment, and insider threat emulation. Customize attack lifecycles to test blue team readiness.

Social Engineering Engine
Generate convincing lures, clone login portals, and automate voice/SMS phishing (vishing/smishing). Track user behavior analytics and bypass MFA with real-time proxy interception.

Network Penetration Testing Commands
Built-in command suite includes:
nmap -sV -sC -O -T4 target
crackmapexec smb target -u users.txt -p passes.txt
responder -I eth0 -wF
msfconsole -q -r resource.rc
Full integration with Metasploit, Empire, and Cobalt Strike (license required).

Nikto Integration
One-click Nikto web scanner: nikto -h https://target.com -ssl -Format html -o scan_report. Automated vulnerability discovery for misconfigurations, outdated servers, and dangerous CGIs.

Network Mapping
Layer 2/3 discovery with ARP spoofing, LLMNR/NBT-NS poisoning, and automated topology graphing. Export maps to GraphML or Visio.

Multi-Channel C2 Communication
Control War Phish from any platform. The agent communicates with your command server via:

* Telegram (bot commands + encrypted callbacks)

* Discord


* Slack (slash commands & webhook alerts)

* iMessage (via PyPush bridge)

* Google Chat (space integration)

* Web Application (full-featured dashboard with live session management)

# Dark Web Links
War Phish includes a curated, read-only list of operational dark web resources (.onion) for threat intelligence, breach data correlation, and adversary infrastructure monitoring. Access requires explicit user enablement and compliance with local laws.

# Who It's For

* White Hat Hackers – authorized assessments, phishing simulations, and compliance testing

* Red Hat Hackers – active counter-hacking and defending compromised networks

* Security Teams – continuous cyber drill orchestration

# Legal & Ethical Use
War Phish is a dual-use tool. Accurate Cyber Defense licenses this software exclusively to verified organizations, pentesting professionals, and researchers. Unauthorized use against systems without explicit written permission is illegal. Red hat usage must comply with active authorization or defensive operations within owned environments.

# Clone repository
```bash
git clone https://github.com/Iankulani/warphish.git
cd warphish
```

# Run installer
```bash
setup.bat
```
# Activate environment

venv\Scripts\activate

# Run WAR PHISH
```bash
python warphish.py
```

# Docker

# Build image
```bash
docker build -t warphish:latest .
```
# Run with docker-compose
```bash
docker-compose up -d
```

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
```
# Bot Configuration
# Discord Bot
```bash
Go to https://discord.com/developers/applications
```
Create new application → Bot

Copy token to .env as DISCORD_TOKEN

Enable Privileged Gateway Intents

# Telegram Bot
Message @BotFather on Telegram

Create new bot with /newbot

Copy token to .env as TELEGRAM_BOT_TOKEN

Get API ID/Hash from https://my.telegram.org

# Slack Bot
```bash
Go to https://api.slack.com/apps
````
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
