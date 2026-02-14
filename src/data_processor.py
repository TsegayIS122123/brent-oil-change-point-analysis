"""
Data processing module for Brent oil price analysis.
Handles loading, cleaning, and preparing time series data.
"""
from datetime import datetime, timedelta
from typing import Tuple, Optional, Dict, List
import pandas as pd
import numpy as np
from dataclasses import dataclass


@dataclass
class DataConfig:
    """Configuration for data processing."""
    price_column: str = "Price"
    date_column: str = "Date"
    date_format: str = "mixed"  # 'mixed' handles multiple formats
    log_returns: bool = True
    test_size: float = 0.2
    random_seed: int = 42


class BrentDataLoader:
    """Load and preprocess Brent oil price data."""
    
    def __init__(self, config: Optional[DataConfig] = None):
        """
        Initialize data loader with configuration.
        
        Args:
            config: DataConfig object with processing parameters
        """
        self.config = config or DataConfig()
        self.raw_data: Optional[pd.DataFrame] = None
        self.processed_data: Optional[pd.DataFrame] = None
        
    def load_data(self, filepath: str) -> pd.DataFrame:
        """
        Load Brent oil prices from CSV file.
        
        Args:
            filepath: Path to CSV file
            
        Returns:
            DataFrame with loaded data
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If required columns missing
        """
        try:
            df = pd.read_csv(filepath)
            print(f"✓ Loaded {len(df)} rows from {filepath}")
        except FileNotFoundError:
            raise FileNotFoundError(f"Data file not found: {filepath}")
            
        # Validate required columns
        required_cols = [self.config.price_column, self.config.date_column]
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
            
        self.raw_data = df
        return df
    
    def parse_dates(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Parse date column with mixed formats.
        
        Handles both '20-May-87' and 'Apr 22, 2020' formats.
        
        Args:
            df: DataFrame with date column
            
        Returns:
            DataFrame with parsed datetime column
        """
        df = df.copy()
        
        # Try parsing with mixed format
        try:
            df['Date_parsed'] = pd.to_datetime(
                df[self.config.date_column], 
                format='mixed'
            )
        except:
            # Fallback: try individual formats
            def parse_date(date_str):
                for fmt in ['%d-%b-%y', '%b %d, %Y', '%Y-%m-%d']:
                    try:
                        return pd.to_datetime(date_str, format=fmt)
                    except:
                        continue
                return pd.NaT
                
            df['Date_parsed'] = df[self.config.date_column].apply(parse_date)
        
        # Drop rows with invalid dates
        initial_len = len(df)
        df = df.dropna(subset=['Date_parsed'])
        if len(df) < initial_len:
            print(f"⚠ Dropped {initial_len - len(df)} rows with invalid dates")
            
        return df
    
    def calculate_log_returns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate log returns from price series.
        
        Args:
            df: DataFrame with price column
            
        Returns:
            DataFrame with added log_return column
        """
        df = df.copy()
        df = df.sort_values('Date_parsed')
        df['Log_Return'] = np.log(
            df[self.config.price_column] / df[self.config.price_column].shift(1)
        )
        df = df.dropna(subset=['Log_Return'])
        return df
    
    def prepare_for_analysis(
        self, 
        df: pd.DataFrame, 
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Prepare data for change point analysis.
        
        Args:
            df: Raw DataFrame
            start_date: Optional start date filter (YYYY-MM-DD)
            end_date: Optional end date filter (YYYY-MM-DD)
            
        Returns:
            Processed DataFrame ready for modeling
        """
        # Parse dates
        df = self.parse_dates(df)
        
        # Filter by date range if provided
        if start_date:
            df = df[df['Date_parsed'] >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df['Date_parsed'] <= pd.to_datetime(end_date)]
            
        # Calculate log returns if requested
        if self.config.log_returns:
            df = self.calculate_log_returns(df)
            
        # Sort by date
        df = df.sort_values('Date_parsed').reset_index(drop=True)
        
        self.processed_data = df
        print(f"✓ Prepared {len(df)} observations for analysis")
        print(f"  Date range: {df['Date_parsed'].min()} to {df['Date_parsed'].max()}")
        
        return df
    
    def split_data(
        self, 
        df: pd.DataFrame, 
        split_date: Optional[str] = None
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Split data into before/after periods.
        
        Args:
            df: Processed DataFrame
            split_date: Date to split at (if None, splits at midpoint)
            
        Returns:
            Tuple of (before_df, after_df)
        """
        if split_date:
            split_dt = pd.to_datetime(split_date)
            before = df[df['Date_parsed'] < split_dt].copy()
            after = df[df['Date_parsed'] >= split_dt].copy()
        else:
            # Split at midpoint
            mid_idx = len(df) // 2
            before = df.iloc[:mid_idx].copy()
            after = df.iloc[mid_idx:].copy()
            
        print(f"✓ Split data: {len(before)} before, {len(after)} after")
        return before, after


class EventDataLoader:
    """Load and process geopolitical events data."""
    
    def __init__(self):
        self.events: Optional[pd.DataFrame] = None
        
    def load_events(self, filepath: str) -> pd.DataFrame:
        """
        Load events from CSV file.
        
        Args:
            filepath: Path to events CSV
            
        Returns:
            DataFrame with events
        """
        events = pd.read_csv(filepath)
        
        # Parse dates if needed
        if 'event_date' in events.columns:
            events['event_date'] = pd.to_datetime(events['event_date'])
            # ALSO CREATE Date_parsed for compatibility
            events['Date_parsed'] = events['event_date']
        elif 'Date' in events.columns:
            events['event_date'] = pd.to_datetime(events['Date'])
            events['Date_parsed'] = events['event_date']
        else:
            # Try to find any date column
            for col in events.columns:
                if 'date' in col.lower():
                    events['event_date'] = pd.to_datetime(events[col])
                    events['Date_parsed'] = events['event_date']
                    break
        
        self.events = events
        print(f"✓ Loaded {len(events)} events")
        return events
    
    def find_events_near_date(
        self, 
        target_date: str, 
        window_days: int = 45
    ) -> pd.DataFrame:
        """
        Find events within window_days of target date.
        
        Args:
            target_date: Date to search around
            window_days: Days before/after to include
            
        Returns:
            DataFrame with nearby events
        """
        if self.events is None:
            raise ValueError("Events not loaded. Call load_events() first.")
        
        # Ensure Date_parsed exists
        if 'Date_parsed' not in self.events.columns:
            if 'event_date' in self.events.columns:
                self.events['Date_parsed'] = self.events['event_date']
            else:
                raise ValueError("No date column found in events data")
        
        target = pd.to_datetime(target_date)
        start = target - timedelta(days=window_days)
        end = target + timedelta(days=window_days)
        
        nearby = self.events[
            (self.events['Date_parsed'] >= start) & 
            (self.events['Date_parsed'] <= end)
        ].copy()
        
        nearby['Days_from_change'] = (nearby['Date_parsed'] - target).dt.days
        
        return nearby.sort_values('Days_from_change')