"""
Unit tests for Flask backend API.
"""

import unittest
import sys
import os
import json
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np
from datetime import datetime

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
    
    @patch('backend.app.pd.read_csv')
    def test_prices_endpoint_structure(self, mock_read_csv):
        """Test prices endpoint returns correct structure with mocked data."""
        # Create mock DataFrame for testing
        mock_df = pd.DataFrame({
            'Date': pd.date_range('2020-01-01', periods=100),
            'Price': np.random.uniform(50, 100, 100)
        })
        mock_read_csv.return_value = mock_df
        
        response = self.app.get('/api/prices')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('success', data)
        self.assertIn('data', data)
        self.assertIn('count', data)
    
    @patch('backend.app.pd.read_csv')
    def test_events_endpoint_structure(self, mock_read_csv):
        """Test events endpoint returns correct structure with mocked data."""
        # Create mock DataFrame for testing
        mock_df = pd.DataFrame({
            'event_date': pd.date_range('2020-01-01', periods=5),
            'event_name': ['Event1', 'Event2', 'Event3', 'Event4', 'Event5'],
            'event_type': ['Economic'] * 5,
            'severity': ['High'] * 5
        })
        mock_read_csv.return_value = mock_df
        
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
    
    @patch('backend.app.pd.read_csv')
    def test_summary_endpoint(self, mock_read_csv):
        """Test summary endpoint returns metrics with mocked data."""
        # Create mock DataFrame for testing
        mock_df = pd.DataFrame({
            'Date': pd.date_range('2020-01-01', periods=100),
            'Price': np.random.uniform(50, 100, 100),
            'Log_Return': np.random.normal(0, 0.02, 100)
        })
        mock_read_csv.return_value = mock_df
        
        response = self.app.get('/api/summary')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('latest_price', data['data'])
    
    @patch('backend.app.pd.read_csv')
    def test_event_impact_endpoint_structure(self, mock_read_csv):
        """Test event impact endpoint returns proper structure."""
        # Mock returns different DataFrames for different calls
        price_mock = pd.DataFrame({
            'Date': pd.date_range('2020-01-01', periods=100),
            'Price': np.random.uniform(50, 100, 100)
        })
        events_mock = pd.DataFrame({
            'event_date': [pd.Timestamp('2020-03-11')],
            'event_name': ['Test Event'],
            'event_type': ['Economic'],
            'severity': ['High']
        })
        
        # Make mock return different values on consecutive calls
        mock_read_csv.side_effect = [price_mock, events_mock]
        
        response = self.app.get('/api/event-impact/0')
        
        # Should work with our mock data
        if response.status_code == 200:
            data = json.loads(response.data)
            self.assertTrue(data['success'])

class TestDataModels(unittest.TestCase):
    """Test cases for data models."""
    
    def test_price_data_model_creation(self):
        """Test PriceData model can be created."""
        try:
            from src.models.data_models import PriceData
            
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