#!/bin/sh
# WAR PHISH - Alpine Linux Dependency Installation Script

set -e

echo "[*] Installing WAR PHISH for Alpine Linux..."

# System dependencies
apk add --no-cache \
    # Python & Build Tools
    python3 py3-pip python3-dev py3-virtualenv \
    gcc musl-dev libffi-dev openssl-dev \
    cargo rust make cmake \
    \
    # Network Tools
    nmap nmap-scripts whois bind-tools \
    curl wget openssh-client netcat-openbsd \
    hping3 arp-scan dsniff macchanger \
    tcpdump iproute2 iptables ip6tables \
    bridge-utils wireguard-tools \
    \
    # System Utilities
    tzdata git build-base sudo \
    bash zsh jq vim nano htop \
    ca-certificates openssl \
    \
    # Database & Cache
    redis mariadb-client postgresql-client sqlite \
    \
    # Monitoring
    procps sysstat lsof strace \
    \
    # Optional Tools
    grep sed awk findutils coreutils

# Create virtual environment
python3 -m venv /opt/warphish/venv
. /opt/warphish/venv/bin/activate

# Upgrade pip
pip install --no-cache-dir --upgrade pip setuptools wheel

# Install Python requirements
if [ -f /opt/warphish/requirements-alpine.txt ]; then
    pip install --no-cache-dir -r /opt/warphish/requirements-alpine.txt
else
    echo "[!] requirements-alpine.txt not found"
    exit 1
fi

# Set proper permissions
chmod +x /opt/warphish/start.sh
chmod -R 755 /opt/warphish

# Create necessary directories
mkdir -p /var/log/warphish
mkdir -p /etc/warphish
mkdir -p /opt/warphish/reports
mkdir -p /opt/warphish/.warphish

echo "[✓] WAR PHISH installation complete!"
echo "[*] Run 'source /opt/warphish/venv/bin/activate' to activate environment"