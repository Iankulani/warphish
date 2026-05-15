#!/usr/bin/env python3
"""
WAR PHISH - Docker Health Check Script
"""

import sys
import socket
import requests

def check_web_server():
    """Check if web server is responding"""
    try:
        response = requests.get("http://localhost:5000", timeout=5)
        return response.status_code == 200
    except:
        return False

def check_phishing_server():
    """Check if phishing server is running"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex(('localhost', 8080))
        sock.close()
        return result == 0
    except:
        return False

def check_database():
    """Check database connectivity"""
    try:
        from warphish import DatabaseManager
        db = DatabaseManager()
        stats = db.get_statistics()
        db.close()
        return True
    except:
        return False

def main():
    """Main health check function"""
    web_ok = check_web_server()
    db_ok = check_database()
    
    if web_ok and db_ok:
        print("✅ WAR PHISH is healthy")
        sys.exit(0)
    else:
        print("❌ WAR PHISH is unhealthy")
        print(f"  Web Server: {'OK' if web_ok else 'FAIL'}")
        print(f"  Database: {'OK' if db_ok else 'FAIL'}")
        sys.exit(1)

if __name__ == "__main__":
    main()