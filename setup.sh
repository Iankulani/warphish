#!/bin/bash
# 🦈 WAR PHISH - Linux/macOS Installation Script
# Run: chmod +x setup.sh && ./setup.sh

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                 🦈 WAR PHISH INSTALLATION                    ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check Python version
echo -e "${YELLOW}[1/6] Checking Python version...${NC}"
if command -v python3 &>/dev/null; then
    PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    if (( $(echo "$PYTHON_VERSION >= 3.7" | bc -l) )); then
        echo -e "${GREEN}✓ Python $PYTHON_VERSION detected${NC}"
    else
        echo -e "${RED}✗ Python 3.7+ required (found $PYTHON_VERSION)${NC}"
        exit 1
    fi
else
    echo -e "${RED}✗ Python3 not found. Please install Python 3.7+${NC}"
    exit 1
fi

# Create virtual environment
echo -e "${YELLOW}[2/6] Creating virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo -e "${YELLOW}[3/6] Upgrading pip...${NC}"
pip install --upgrade pip setuptools wheel

# Install requirements
echo -e "${YELLOW}[4/6] Installing Python dependencies...${NC}"
pip install -r requirements.txt

# Install system tools (Linux only)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo -e "${YELLOW}[5/6] Installing system tools...${NC}"
    
    if command -v apt-get &>/dev/null; then
        sudo apt-get update
        sudo apt-get install -y \
            nmap \
            hping3 \
            dsniff \
            macchanger \
            tcpdump \
            netcat-openbsd \
            whois \
            dnsutils \
            curl \
            wget \
            ssh \
            python3-pip \
            build-essential \
            libpcap-dev \
            tshark
    elif command -v yum &>/dev/null; then
        sudo yum install -y \
            nmap \
            hping3 \
            dsniff \
            macchanger \
            tcpdump \
            nc \
            whois \
            bind-utils \
            curl \
            wget \
            openssh-clients \
            python3-devel \
            libpcap-devel
    elif command -v brew &>/dev/null; then
        brew install \
            nmap \
            hping3 \
            dsniff \
            macchanger \
            tcpdump \
            netcat \
            whois \
            curl \
            wget
    fi
    
    # Install signal-cli for Signal bot
    if command -v apt-get &>/dev/null; then
        wget -qO- https://raw.githubusercontent.com/AsamK/signal-cli/master/install.sh | sudo bash
    fi
fi

# Create directories
echo -e "${YELLOW}[6/6] Creating directories...${NC}"
mkdir -p .warphish
mkdir -p reports
mkdir -p logs
mkdir -p phishing_pages
mkdir -p wordlists
mkdir -p captured_credentials

# Create .env file
if [ ! -f .env ]; then
    cp .env.example .env
    echo -e "${GREEN}✓ Created .env file (edit with your tokens)${NC}"
fi

# Set permissions
chmod +x warphish.py
chmod +x scripts/*.sh

# Done
echo -e "${GREEN}"
echo "════════════════════════════════════════════════════════════════"
echo "                    ✅ INSTALLATION COMPLETE!                    "
echo "════════════════════════════════════════════════════════════════"
echo -e "${NC}"
echo -e "${BLUE}Next steps:${NC}"
echo "  1. Edit .env file with your bot tokens"
echo "  2. Activate environment: source venv/bin/activate"
echo "  3. Run WAR PHISH: python3 warphish.py"
echo "  4. Access web dashboard: http://localhost:5000"
echo ""
echo -e "${YELLOW}⚠️  Run as root for full functionality (spoofing, packet capture)${NC}"