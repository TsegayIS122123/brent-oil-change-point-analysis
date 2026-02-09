"""
Data processing utilities for Brent Oil analysis.
Includes data cleaning, transformation, and validation.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Tuple, List, Dict
import logging

logger = logging.getLogger(__name__)

class DataProcessor:
    """Processor for Brent oil price data."""
    
    @staticmethod
    def load_and_clean_data(filepath: str) -> pd.DataFrame:
        """
        Load and clean Brent oil price data.
        
        Args:
            filepath: Path to CSV file
            
        Returns:
            Cleaned DataFrame with Date and Price columns
        """
        try:
            # Load data
            df = pd.read_csv(filepath)
            logger.info(f"Loaded {len(df)} records from {filepath}")
            
            # Clean column names
            df.columns = [col.strip() for col in df.columns]
            
            # Parse dates (handle multiple formats)
            df['Date'] = pd.to_datetime(df['Date'], format='mixed', errors='coerce')
            
            # Drop rows with invalid dates
            initial_count = len(df)
            df = df.dropna(subset=['Date'])
            if len(df) < initial_count:
                logger.warning(f"Dropped {initial_count - len(df)} rows with invalid dates")
            
            # Ensure Price is numeric
            df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
            df = df.dropna(subset=['Price'])
            
            # Sort by date
            df = df.sort_values('Date').reset_index(drop=True)
            
            # Calculate log returns
            df['Log_Return'] = np.log(df['Price'] / df['Price'].shift(1))
            
            logger.info(f"Data cleaning complete. Final dataset: {len(df)} records")
            return df
            
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
    
    @staticmethod
    def calculate_summary_stats(df: pd.DataFrame) -> Dict:
        """
        Calculate summary statistics from price data.
        
        Args:
            df: DataFrame with Price and Log_Return columns
            
        Returns:
            Dictionary of summary statistics
        """
        if df.empty:
            return {}
        
        stats = {
            'latest_price': float(df['Price'].iloc[-1]),
            'average_price': float(df['Price'].mean()),
            'min_price': float(df['Price'].min()),
            'max_price': float(df['Price'].max()),
            'price_range': float(df['Price'].max() - df['Price'].min()),
            'volatility': float(df['Log_Return'].std() if 'Log_Return' in df.columns else 0),
            'total_days': len(df),
            'date_range': {
                'start': df['Date'].min().strftime('%Y-%m-%d'),
                'end': df['Date'].max().strftime('%Y-%m-%d')
            }
        }
        
        # Calculate annualized return if enough data
        if len(df) > 1:
            first_price = df['Price'].iloc[0]
            last_price = df['Price'].iloc[-1]
            total_return = (last_price - first_price) / first_price
            
            # Calculate years difference
            days_diff = (df['Date'].iloc[-1] - df['Date'].iloc[0]).days
            years_diff = days_diff / 365.25
            
            if years_diff > 0:
                stats['annualized_return_pct'] = float(((1 + total_return) ** (1/years_diff) - 1) * 100)
        
        return stats
    
    @staticmethod
    def filter_by_date_range(df: pd.DataFrame, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Filter DataFrame by date range.
        
        Args:
            df: Input DataFrame
            start_date: Start date string (YYYY-MM-DD)
            end_date: End date string (YYYY-MM-DD)
            
        Returns:
            Filtered DataFrame
        """
        mask = (df['Date'] >= pd.to_datetime(start_date)) & \
               (df['Date'] <= pd.to_datetime(end_date))
        return df[mask].copy()
    
    @staticmethod
    def calculate_event_impact(price_df: pd.DataFrame, event_date: datetime, 
                              window_days: int = 30) -> Dict:
        """
        Calculate impact of an event on oil prices.
        
        Args:
            price_df: Price DataFrame
            event_date: Event date
            window_days: Days before/after event to analyze
            
        Returns:
            Impact analysis dictionary
        """
        # Define analysis window
        start_date = event_date - timedelta(days=window_days)
        end_date = event_date + timedelta(days=window_days)
        
        # Filter data in window
        window_df = price_df[
            (price_df['Date'] >= start_date) & 
            (price_df['Date'] <= end_date)
        ].copy()
        
        if len(window_df) == 0:
            return {}
        
        # Split before/after event
        before_event = window_df[window_df['Date'] < event_date]
        after_event = window_df[window_df['Date'] > event_date]
        
        if len(before_event) == 0 or len(after_event) == 0:
            return {}
        
        # Calculate metrics
        price_before = float(before_event['Price'].mean())
        price_after = float(after_event['Price'].mean())
        price_change = price_after - price_before
        price_change_pct = (price_change / price_before * 100) if price_before > 0 else 0
        
        return {
            'before_event': price_before,
            'after_event': price_after,
            'absolute_change': price_change,
            'percentage_change': price_change_pct,
            'window_days': window_days,
            'analysis_window': {
                'start': start_date.strftime('%Y-%m-%d'),
                'end': end_date.strftime('%Y-%m-%d')
            }
        }