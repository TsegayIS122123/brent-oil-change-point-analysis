"""
Unit tests for data processing module.
Run with: pytest tests/test_data_processor.py -v
"""
import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_processor import BrentDataLoader, DataConfig, EventDataLoader


class TestBrentDataLoader:
    """Test suite for BrentDataLoader class."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample data with mixed date formats."""
        return pd.DataFrame({
            'Date': ['20-May-87', '21-May-87', '22-May-87', 'Apr 22, 2020', 'Apr 23, 2020'],
            'Price': [18.63, 18.45, 18.55, 13.77, 15.06]
        })
    
    @pytest.fixture
    def temp_csv_file(self, tmp_path, sample_data):
        """Create temporary CSV file."""
        filepath = tmp_path / "test_prices.csv"
        sample_data.to_csv(filepath, index=False)
        return str(filepath)
    
    def test_1_initialization(self):
        """Test that DataLoader initializes with correct config."""
        config = DataConfig(
            price_column="Price",
            date_column="Date",
            log_returns=True
        )
        loader = BrentDataLoader(config)
        
        assert loader.config.price_column == "Price"
        assert loader.config.date_column == "Date"
        assert loader.config.log_returns is True
        assert loader.raw_data is None
        assert loader.processed_data is None
        print("✓ test_1_initialization passed")
    
    def test_2_load_data(self, temp_csv_file):
        """Test loading data from CSV file."""
        loader = BrentDataLoader()
        df = loader.load_data(temp_csv_file)
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 5
        assert 'Price' in df.columns
        assert 'Date' in df.columns
        print("✓ test_2_load_data passed")
    
    def test_3_load_data_file_not_found(self):
        """Test error handling for missing file."""
        loader = BrentDataLoader()
        
        with pytest.raises(FileNotFoundError) as exc_info:
            loader.load_data("nonexistent_file.csv")
        
        assert "not found" in str(exc_info.value)
        print("✓ test_3_load_data_file_not_found passed")
    
    def test_4_parse_dates_mixed_format(self, sample_data):
        """Test parsing mixed date formats (both '20-May-87' and 'Apr 22, 2020')."""
        loader = BrentDataLoader()
        parsed = loader.parse_dates(sample_data)
        
        assert 'Date_parsed' in parsed.columns
        assert pd.api.types.is_datetime64_any_dtype(parsed['Date_parsed'])
        
        # Check first date (20-May-87 format)
        assert parsed['Date_parsed'].iloc[0].year == 1987
        assert parsed['Date_parsed'].iloc[0].month == 5
        assert parsed['Date_parsed'].iloc[0].day == 20
        
        # Check date with Apr 22, 2020 format
        assert parsed['Date_parsed'].iloc[3].year == 2020
        assert parsed['Date_parsed'].iloc[3].month == 4
        assert parsed['Date_parsed'].iloc[3].day == 22
        print("✓ test_4_parse_dates_mixed_format passed")
    
    def test_5_calculate_log_returns(self, sample_data):
        """Test log return calculation."""
        loader = BrentDataLoader()
        parsed = loader.parse_dates(sample_data)
        with_returns = loader.calculate_log_returns(parsed)
        
        assert 'Log_Return' in with_returns.columns
        assert len(with_returns) == len(parsed) - 1  # First row has NaN return
        
        # Check log return calculation between first two prices
        price1 = parsed['Price'].iloc[0]
        price2 = parsed['Price'].iloc[1]
        expected_return = np.log(price2 / price1)
        actual_return = with_returns['Log_Return'].iloc[0]
        
        assert abs(actual_return - expected_return) < 1e-10
        print("✓ test_5_calculate_log_returns passed")
    
    def test_6_prepare_for_analysis(self, temp_csv_file):
        """Test full data preparation pipeline."""
        loader = BrentDataLoader(DataConfig(log_returns=True))
        raw = loader.load_data(temp_csv_file)
        processed = loader.prepare_for_analysis(raw)
        
        assert len(processed) > 0
        assert 'Date_parsed' in processed.columns
        assert 'Log_Return' in processed.columns
        
        # Check that dates are sorted
        dates = processed['Date_parsed']
        assert dates.is_monotonic_increasing
        print("✓ test_6_prepare_for_analysis passed")
    
    def test_7_split_data(self, sample_data):
        """Test splitting data before/after a date."""
        loader = BrentDataLoader()
        parsed = loader.parse_dates(sample_data)
        
        # Split at 2000-01-01 (between 1987 and 2020 data)
        before, after = loader.split_data(parsed, split_date='2000-01-01')
        
        assert len(before) == 3  # 1987 dates
        assert len(after) == 2    # 2020 dates
        
        # Check that before dates are all < 2000
        assert all(before['Date_parsed'] < pd.to_datetime('2000-01-01'))
        
        # Check that after dates are all >= 2000
        assert all(after['Date_parsed'] >= pd.to_datetime('2000-01-01'))
        print("✓ test_7_split_data passed")


class TestEventDataLoader:
    """Test suite for EventDataLoader class."""
    
    @pytest.fixture
    def sample_events(self):
        """Create sample events for testing."""
        return pd.DataFrame({
            'event_date': ['1990-08-02', '2001-09-11', '2008-07-11', '2020-01-02', '2022-02-24'],
            'event_name': [
                'Iraq invades Kuwait',
                '9/11 Attacks',
                'Global Financial Crisis',
                'COVID-19 Pandemic',
                'Russia invades Ukraine'
            ],
            'event_type': [
                'Geopolitical Conflict',
                'Geopolitical',
                'Economic',
                'Economic',
                'Geopolitical Conflict'
            ],
            'severity': ['Very High', 'Very High', 'Very High', 'Very High', 'Very High']
        })
    
    @pytest.fixture
    def temp_events_file(self, tmp_path, sample_events):
        """Create temporary events CSV file."""
        filepath = tmp_path / "test_events.csv"
        sample_events.to_csv(filepath, index=False)
        return str(filepath)
    
    def test_8_load_events(self, temp_events_file):
        """Test loading events from CSV."""
        loader = EventDataLoader()
        events = loader.load_events(temp_events_file)
        
        assert len(events) == 5
        assert 'event_date' in events.columns
        assert 'event_name' in events.columns
        assert 'event_type' in events.columns
        print("✓ test_8_load_events passed")
    
    def test_9_find_events_near_date(self, temp_events_file):
        """Test finding events near a target date."""
        loader = EventDataLoader()
        loader.load_events(temp_events_file)
        
        # Find events near COVID-19 date
        nearby = loader.find_events_near_date('2020-01-02', window_days=30)
        
        assert len(nearby) >= 1
        assert 'COVID-19' in nearby['event_name'].iloc[0]
        
        # Check days calculation
        assert 'Days_from_change' in nearby.columns
        print("✓ test_9_find_events_near_date passed")
    
    def test_10_no_events_near_date(self, temp_events_file):
        """Test when no events are near target date."""
        loader = EventDataLoader()
        loader.load_events(temp_events_file)
        
        # Date far from any events
        nearby = loader.find_events_near_date('2010-01-01', window_days=30)
        
        assert len(nearby) == 0
        print("✓ test_10_no_events_near_date passed")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])