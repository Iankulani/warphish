# 🦈 WAR PHISH - Installation Guide

## System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | 2 cores | 4+ cores |
| RAM | 2 GB | 4+ GB |
| Storage | 1 GB | 10+ GB |
| Python | 3.7+ | 3.11+ |
| OS | Linux/macOS/Windows | Ubuntu 22.04 LTS |

## Quick Installation

### Linux / macOS

```bash
# Clone repository
git clone https://github.com/Iankulani/warphish.git
cd warphish

# Run installer
chmod +x setup.sh
./setup.sh

# Activate environment
source venv/bin/activate

# Run WAR PHISH
python3 warphish.py