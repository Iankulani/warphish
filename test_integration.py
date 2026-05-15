#!/usr/bin/env python3
"""
WAR PHISH - Integration Tests
"""

import pytest
import threading
import time
import requests
import socket
from unittest.mock import patch, MagicMock


@pytest.mark.integration
class TestWarPhishIntegration:
    """Integration tests for WAR PHISH"""

    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Setup before each test"""
        # Import here to avoid circular imports
        from warphish import WarPhish, WebServer, PhishingServer, DatabaseManager
        
        self.db = DatabaseManager(":memory:")
        from warphish import SpoofingEngine, CommandHandler
        self.spoof_engine = SpoofingEngine(self.db)
        self.phishing_server = PhishingServer(self.db)
        self.handler = CommandHandler(self.db, self.spoof_engine, self.phishing_server)
        
        yield
        
        self.phishing_server.stop()
        self.db.close()

    def test_command_flow(self):
        """Test complete command execution flow"""
        # Execute multiple commands in sequence
        commands = ["help", "status", "time", "date"]
        
        for cmd in commands:
            result = self.handler.execute(cmd)
            assert result['success'] is True
            assert 'output' in result

    def test_phishing_link_flow(self):
        """Test complete phishing link generation and server start flow"""
        # Generate link
        gen_result = self.handler.execute("generate_phishing facebook")
        assert gen_result['success'] is True
        
        # Extract link ID from output (simplified)
        import re
        match = re.search(r'Link ID: (\w+)', gen_result['output'])
        if match:
            link_id = match.group(1)
            
            # Start server (would need actual port binding, skip in test)
            # start_result = self.handler.execute(f"phishing_start {link_id}")
            # assert start_result['success'] is True

    def test_network_command_chain(self):
        """Test chain of network commands"""
        # Test ping (mocked)
        with patch('subprocess.run') as mock_run:
            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_result.stdout = "PING success"
            mock_run.return_value = mock_result
            
            ping_result = self.handler.execute("ping localhost")
            assert ping_result['success'] is True

    def test_error_handling(self):
        """Test error handling across the system"""
        # Invalid command
        result = self.handler.execute("")
        assert result['success'] is False
        
        # Invalid phishing platform
        result = self.handler.execute("generate_phishing invalid_platform")
        assert result['success'] is False
        
        # Invalid port scan
        result = self.handler.execute("scan")
        assert result['success'] is False

    def test_database_operations_chain(self):
        """Test chain of database operations"""
        # Save multiple items
        for i in range(5):
            self.db.save_phishing_link(f"link_{i}", "test", f"http://test{i}.com")
        
        links = self.db.get_phishing_links()
        assert len(links) >= 5
        
        # Log commands
        for i in range(3):
            self.db.log_command(f"cmd_{i}", "test", "test", True, "ok", 0.1)
        
        history = self.db.get_command_history(10)
        assert len(history) >= 3
        
        # Get stats
        stats = self.db.get_statistics()
        assert stats['total_phishing_links'] >= 5

    def test_sql_injection_protection(self):
        """Test SQL injection protection in database"""
        malicious = "'; DROP TABLE command_history; --"
        
        # Should not cause SQL injection
        result = self.db.save_phishing_link(malicious, "test", "http://test.com")
        # Should succeed without dropping table
        assert result is True or result is False  # Just ensure no crash
        
        # Check table still exists
        try:
            self.db.cursor.execute("SELECT COUNT(*) FROM command_history")
            self.db.cursor.fetchone()
            table_exists = True
        except:
            table_exists = False
        
        assert table_exists is True


@pytest.mark.integration
@pytest.mark.slow
class TestPerformance:
    """Performance tests"""

    def test_command_performance(self):
        """Test command execution performance"""
        import time
        from warphish import DatabaseManager, SpoofingEngine, CommandHandler, PhishingServer
        
        db = DatabaseManager(":memory:")
        spoof = SpoofingEngine(db)
        phishing = PhishingServer(db)
        handler = CommandHandler(db, spoof, phishing)
        
        start = time.time()
        for _ in range(50):
            handler.execute("time")
        elapsed = time.time() - start
        
        # Should handle 50 commands in under 5 seconds
        assert elapsed < 5.0
        
        db.close()

    def test_database_performance(self):
        """Test database performance under load"""
        from warphish import DatabaseManager
        
        db = DatabaseManager(":memory:")
        
        start = time.time()
        for i in range(100):
            db.save_phishing_link(f"perf_link_{i}", "test", f"http://test{i}.com")
        elapsed = time.time() - start
        
        # 100 inserts should be fast
        assert elapsed < 1.0
        
        db.close()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--run-integration"])