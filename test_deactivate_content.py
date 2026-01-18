#!/usr/bin/env python3
"""
Basic tests for the Amazon Kids Content Deactivator
"""

import unittest
import os
from unittest.mock import Mock, patch, MagicMock
from deactivate_content import AmazonKidsContentDeactivator


class TestAmazonKidsContentDeactivator(unittest.TestCase):
    """Test cases for AmazonKidsContentDeactivator class."""
    
    @patch.dict(os.environ, {
        'AMAZON_EMAIL': 'test@example.com',
        'AMAZON_PASSWORD': 'testpass123'
    })
    def test_initialization_with_credentials(self):
        """Test that the deactivator initializes correctly with credentials."""
        deactivator = AmazonKidsContentDeactivator()
        self.assertEqual(deactivator.email, 'test@example.com')
        self.assertEqual(deactivator.password, 'testpass123')
        self.assertEqual(deactivator.unchecked_count, 0)
        
    @patch.dict(os.environ, {}, clear=True)
    def test_initialization_without_credentials_raises_error(self):
        """Test that initialization fails without credentials."""
        with self.assertRaises(ValueError) as context:
            AmazonKidsContentDeactivator()
        self.assertIn('AMAZON_EMAIL and AMAZON_PASSWORD must be set', str(context.exception))
        
    @patch.dict(os.environ, {
        'AMAZON_EMAIL': 'test@example.com',
        'AMAZON_PASSWORD': 'testpass123',
        'PAGE_LOAD_TIMEOUT': '60',
        'ELEMENT_WAIT_TIMEOUT': '20',
        'HEADLESS': 'true'
    })
    def test_configuration_from_environment(self):
        """Test that configuration is correctly read from environment variables."""
        deactivator = AmazonKidsContentDeactivator()
        self.assertEqual(deactivator.page_load_timeout, 60)
        self.assertEqual(deactivator.element_wait_timeout, 20)
        self.assertTrue(deactivator.headless)
        
    @patch.dict(os.environ, {
        'AMAZON_EMAIL': 'test@example.com',
        'AMAZON_PASSWORD': 'testpass123'
    })
    @patch('deactivate_content.webdriver.Chrome')
    @patch('deactivate_content.ChromeDriverManager')
    def test_setup_driver(self, mock_driver_manager, mock_chrome):
        """Test that WebDriver is set up correctly."""
        mock_driver_instance = MagicMock()
        mock_chrome.return_value = mock_driver_instance
        
        deactivator = AmazonKidsContentDeactivator()
        deactivator.setup_driver()
        
        self.assertIsNotNone(deactivator.driver)
        self.assertIsNotNone(deactivator.wait)
        mock_driver_instance.set_page_load_timeout.assert_called_once()
        mock_driver_instance.maximize_window.assert_called_once()
        

class TestHelperMethods(unittest.TestCase):
    """Test helper methods of the deactivator."""
    
    @patch.dict(os.environ, {
        'AMAZON_EMAIL': 'test@example.com',
        'AMAZON_PASSWORD': 'testpass123'
    })
    def setUp(self):
        """Set up test fixtures."""
        self.deactivator = AmazonKidsContentDeactivator()
        self.deactivator.driver = MagicMock()
        
    def test_scroll_to_bottom_detects_height_change(self):
        """Test scroll detection when page height changes."""
        # Mock return values for scroll height - need 3 calls: get initial, scroll, get new
        self.deactivator.driver.execute_script.side_effect = [1000, None, 1500]
        
        result = self.deactivator.scroll_to_bottom()
        
        self.assertTrue(result)
        self.assertEqual(self.deactivator.driver.execute_script.call_count, 3)
        
    def test_scroll_to_bottom_detects_no_change(self):
        """Test scroll detection when page height doesn't change."""
        # Mock same scroll height - need 3 calls: get initial, scroll, get new
        self.deactivator.driver.execute_script.side_effect = [1000, None, 1000]
        
        result = self.deactivator.scroll_to_bottom()
        
        self.assertFalse(result)
        

def run_tests():
    """Run all tests."""
    unittest.main(verbosity=2)


if __name__ == '__main__':
    run_tests()
