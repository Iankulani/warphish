#!/usr/bin/env python3
"""Check if all requirements are properly installed on Alpine Linux"""

import subprocess
import sys
import importlib

REQUIREMENTS = [
    'cryptography', 'requests', 'paramiko', 'flask',
    'flask_socketio', 'scapy', 'bs4',  # beautifulsoup4 is imported as bs4
    'lxml', 'qrcode', 'PIL', 'aiohttp', 'dotenv', 'colorama',
    'yaml', 'loguru', 'psutil', 'socketio', 'eventlet'
]

# Map package names to their import names
IMPORT_NAMES = {
    'flask': 'flask',
    'flask_socketio': 'flask_socketio',
    'beautifulsoup4': 'bs4',  # Special case
    'PIL': 'PIL',
    'dotenv': 'dotenv',
    'scapy': 'scapy',
    'cryptography': 'cryptography',
    'requests': 'requests',
    'paramiko': 'paramiko',
    'lxml': 'lxml',
    'qrcode': 'qrcode',
    'aiohttp': 'aiohttp',
    'colorama': 'colorama',
    'yaml': 'yaml',
    'loguru': 'loguru',
    'psutil': 'psutil',
    'socketio': 'socketio',
    'eventlet': 'eventlet'
}

def check_system_packages():
    """Check Alpine system packages"""
    system_packages = [
        'nmap', 'whois', 'bind-tools', 'curl', 'wget',
        'netcat-openbsd', 'hping3', 'arp-scan', 'tcpdump'
    ]
    
    for pkg in system_packages:
        try:
            result = subprocess.run(['apk', 'info', '-e', pkg], 
                                   capture_output=True, text=True, 
                                   check=False)  # Don't raise exception on non-zero exit
            if result.returncode == 0:
                print(f"✓ {pkg}")
            else:
                print(f"✗ {pkg} (not installed)")
        except FileNotFoundError:
            print(f"⚠ apk command not found - not on Alpine Linux?")
            return
        except Exception as e:
            print(f"✗ {pkg} (error: {e})")

def check_python_packages():
    """Check Python packages"""
    for pkg_name in REQUIREMENTS:
        # Get the correct import name
        import_name = IMPORT_NAMES.get(pkg_name, pkg_name)
        
        try:
            importlib.import_module(import_name)
            print(f"✓ {pkg_name}")
        except ImportError:
            print(f"✗ {pkg_name} (missing)")

def main():
    print("=== WAR PHISH Dependency Check for Alpine ===\n")
    print("System Packages:")
    check_system_packages()
    print("\nPython Packages:")
    check_python_packages()
    print("\n✓ Validation complete")

if __name__ == '__main__':
    main()