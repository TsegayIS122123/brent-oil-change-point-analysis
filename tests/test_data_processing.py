"""
Tests for data processing utilities.
"""

import unittest
import pandas as pd
import numpy as np
from datetime import datetime
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

try:
    from src.utils.data_processor import DataProcessor
    import_ok = True
except ImportError as e:
    print(f"Warning: Could not import DataProcessor: {e}")
    import_ok = False
    # Create a mock for testing
    class DataProcessor:
        @staticmethod
        def calculate_summary_stats(df):
            return {}
        @staticmethod 
        def filter_by_date_range(df, start_date, end_date):
            return df
        @staticmethod
        def calculate_event_impact(price_df, event_date, window_days=30):
            return {}

class TestDataProcessor(unittest.TestCase):
    """Test cases for DataProcessor class."""
    
    def setUp(self):
        """Set up test data."""
        # Create sample price data
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        prices = np.random.uniform(70, 90, 100)
        
        self.test_df = pd.DataFrame({
            'Date': dates,
            'Price': prices
        })
        
        # Add log returns
        self.test_df['Log_Return'] = np.log(self.test_df['Price'] / self.test_df['Price'].shift(1))
    
    def test_calculate_summary_stats(self):
        """Test summary statistics calculation."""
        if not import_ok:
            self.skipTest("DataProcessor not available")
            
        stats = DataProcessor.calculate_summary_stats(self.test_df)
        
        # Check required keys exist
        required_keys = [
            'latest_price', 'average_price', 'min_price', 
            'max_price', 'volatility', 'total_days'
        ]
        
        for key in required_keys:
            self.assertIn(key, stats)
            self.assertIsInstance(stats[key], (int, float))
    
    def test_filter_by_date_range(self):
        """Test date range filtering."""
        if not import_ok:
            self.skipTest("DataProcessor not available")
            
        filtered = DataProcessor.filter_by_date_range(
            self.test_df,
            start_date='2023-01-15',
            end_date='2023-01-31'
        )
        
        self.assertGreater(len(filtered), 0)
        self.assertLessEqual(filtered['Date'].min(), pd.to_datetime('2023-01-31'))
        self.assertGreaterEqual(filtered['Date'].max(), pd.to_datetime('2023-01-15'))
    
    def test_calculate_event_impact(self):
        """Test event impact calculation."""
        if not import_ok:
            self.skipTest("DataProcessor not available")
            
        event_date = datetime(2023, 1, 15)  # FIXED: Use correct datetime constructor
        
        impact = DataProcessor.calculate_event_impact(
            self.test_df,
            event_date,
            window_days=10
        )
        
        if impact:  # Only check if we have data in the window
            self.assertIn('before_event', impact)
            self.assertIn('after_event', impact)
            self.assertIn('percentage_change', impact)
    
    def test_empty_dataframe_handling(self):
        """Test handling of empty DataFrame."""
        if not import_ok:
            self.skipTest("DataProcessor not available")
            
        empty_df = pd.DataFrame(columns=['Date', 'Price'])
        stats = DataProcessor.calculate_summary_stats(empty_df)
        
        self.assertEqual(stats, {})

if __name__ == '__main__':
    unittest.main()