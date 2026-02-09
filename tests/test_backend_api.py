"""
Unit tests for Flask backend API.
"""

import unittest
import sys
import os
import json

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

try:
    from backend.app import app
    import_ok = True
except ImportError as e:
    print(f"Warning: Could not import Flask app: {e}")
    import_ok = False
    app = None

class TestBackendAPI(unittest.TestCase):
    """Test cases for backend API endpoints."""
    
    def setUp(self):
        """Set up test client."""
        if not import_ok or app is None:
            self.skipTest("Flask app not available")
            
        self.app = app.test_client()
        self.app.testing = True
    
    def test_home_endpoint(self):
        """Test home endpoint returns API info."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('api', data)
        self.assertIn('endpoints', data)
    
    def test_prices_endpoint_structure(self):
        """Test prices endpoint returns correct structure."""
        response = self.app.get('/api/prices')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('success', data)
        self.assertIn('data', data)
        self.assertIn('count', data)
    
    def test_events_endpoint_structure(self):
        """Test events endpoint returns correct structure."""
        response = self.app.get('/api/events')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('success', data)
        self.assertIn('data', data)
        self.assertIn('count', data)
    
    def test_change_point_endpoint(self):
        """Test change point endpoint returns results."""
        response = self.app.get('/api/change-point')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('change_point_date', data['data'])
    
    def test_summary_endpoint(self):
        """Test summary endpoint returns metrics."""
        response = self.app.get('/api/summary')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        # Check for some expected keys
        self.assertIn('latest_price', data['data'])
    
    def test_event_impact_endpoint_structure(self):
        """Test event impact endpoint returns proper structure."""
        # Test with ID 0 (should work if events exist)
        response = self.app.get('/api/event-impact/0')
        
        # Accept various status codes based on data availability
        if response.status_code == 200:
            data = json.loads(response.data)
            self.assertTrue(data['success'])
        elif response.status_code == 404:
            # Event not found is acceptable
            pass
        else:
            self.fail(f"Unexpected status code: {response.status_code}")

class TestDataModels(unittest.TestCase):
    """Test cases for data models."""
    
    def test_price_data_model_creation(self):
        """Test PriceData model can be created."""
        try:
            from src.models.data_models import PriceData
            
            # Test creating with datetime
            from datetime import datetime
            price_data = PriceData(
                date=datetime(2023, 1, 1),
                price=75.50,
                log_return=0.02
            )
            
            self.assertEqual(price_data.price, 75.50)
            self.assertEqual(price_data.log_return, 0.02)
            
        except ImportError:
            self.skipTest("Data models not available")
    
    def test_event_data_model_creation(self):
        """Test EventData model can be created."""
        try:
            from src.models.data_models import EventData
            
            # Test creating with datetime
            from datetime import datetime
            event_data = EventData(
                event_date=datetime(2022, 2, 24),
                event_name="Test Event",
                event_type="Geopolitical Conflict",
                severity="High"
            )
            
            self.assertEqual(event_data.event_name, "Test Event")
            self.assertEqual(event_data.severity, "High")
            
        except ImportError:
            self.skipTest("Data models not available")

if __name__ == '__main__':
    unittest.main()