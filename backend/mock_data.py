"""
Mock data generator for Brent Oil API.
Provides realistic fallback data when CSV files are not available.
Compatible with Python 3.11+ and Render deployment.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_mock_price_data(n_days=1000):
    """
    Generate realistic mock oil price data based on historical patterns.
    
    Args:
        n_days: Number of days to generate (default: 1000)
    
    Returns:
        DataFrame with Date, Price, and Log_Return columns
    """
    print(f"📊 Generating {n_days} days of mock price data...")
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=n_days)
    
    dates = pd.date_range(start_date, end_date, periods=n_days)
    
    # Set seed for reproducibility
    np.random.seed(42)
    
    # Start at realistic price
    prices = [68.96]  # Starting at detected change point price
    
    # Generate realistic returns with volatility clustering
    for i in range(1, n_days):
        # Random return with slight positive drift
        daily_return = np.random.normal(0.0002, 0.025)
        
        # Add some autocorrelation (volatility clustering)
        if i > 30 and np.std(prices[-30:]) > 2.0:
            daily_return = np.random.normal(0.0001, 0.035)  # Higher volatility
        
        new_price = prices[-1] * (1 + daily_return)
        
        # Keep prices within realistic range ($20 - $150)
        new_price = max(min(new_price, 150.0), 20.0)
        prices.append(new_price)
    
    df = pd.DataFrame({
        'Date': dates,
        'Price': [round(p, 2) for p in prices]
    })
    
    # Add log returns
    df['Log_Return'] = np.log(df['Price'] / df['Price'].shift(1))
    
    print(f"✅ Generated {len(df)} mock price records")
    print(f"   Date range: {df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}")
    print(f"   Price range: ${df['Price'].min():.2f} to ${df['Price'].max():.2f}")
    
    return df

def generate_mock_events():
    """
    Generate mock geopolitical/economic events.
    
    Returns:
        DataFrame with event data
    """
    print("📋 Generating mock events data...")
    
    events = [
        {
            'event_date': pd.Timestamp('2020-03-11'),
            'event_name': 'COVID-19 Pandemic Declared',
            'event_type': 'Economic',
            'severity': 'Very High',
            'region': 'Global',
            'description': 'WHO declares COVID-19 a global pandemic'
        },
        {
            'event_date': pd.Timestamp('2020-04-20'),
            'event_name': 'Negative WTI Oil Prices',
            'event_type': 'Economic',
            'severity': 'Very High',
            'region': 'USA',
            'description': 'WTI crude futures fall below zero for first time'
        },
        {
            'event_date': pd.Timestamp('2021-04-02'),
            'event_name': 'OPEC+ Production Increase',
            'event_type': 'OPEC Policy',
            'severity': 'High',
            'region': 'Global',
            'description': 'OPEC+ agrees to gradually increase production'
        },
        {
            'event_date': pd.Timestamp('2021-03-23'),
            'event_name': 'Suez Canal Blockage',
            'event_type': 'Economic',
            'severity': 'High',
            'region': 'Middle East',
            'description': 'Ever Given container ship blocks Suez Canal'
        },
        {
            'event_date': pd.Timestamp('2021-05-01'),
            'event_name': 'India COVID-19 Second Wave',
            'event_type': 'Economic',
            'severity': 'High',
            'region': 'Asia',
            'description': 'India reports record COVID-19 cases'
        },
        {
            'event_date': pd.Timestamp('2022-02-24'),
            'event_name': 'Russia-Ukraine War',
            'event_type': 'Geopolitical Conflict',
            'severity': 'Very High',
            'region': 'Europe',
            'description': 'Russia invades Ukraine'
        },
        {
            'event_date': pd.Timestamp('2022-03-08'),
            'event_name': 'US Bans Russian Oil',
            'event_type': 'Economic Sanctions',
            'severity': 'High',
            'region': 'Global',
            'description': 'US announces ban on Russian oil imports'
        },
        {
            'event_date': pd.Timestamp('2022-11-01'),
            'event_name': 'OPEC+ Production Cut',
            'event_type': 'OPEC Policy',
            'severity': 'High',
            'region': 'Global',
            'description': 'OPEC+ announces 2 million barrel per day cut'
        },
        {
            'event_date': pd.Timestamp('2019-09-14'),
            'event_name': 'Drone Attacks on Saudi Oil Facilities',
            'event_type': 'Geopolitical Conflict',
            'severity': 'Very High',
            'region': 'Middle East',
            'description': 'Attack cuts Saudi oil production by 50%'
        },
        {
            'event_date': pd.Timestamp('2020-01-02'),
            'event_name': 'COVID-19 Emergency',
            'event_type': 'Economic',
            'severity': 'Very High',
            'region': 'Global',
            'description': 'Global health emergency declared'
        }
    ]
    
    df = pd.DataFrame(events)
    return df

# Pre-calculated change point results from actual Task 2 analysis
MOCK_CHANGE_POINT_RESULTS = {
    "change_point_date": "2021-04-30",
    "price_before": 52.31,
    "price_after": 68.96,
    "price_change_pct": 31.8,
    "return_before": -0.001792,
    "return_after": 0.004035,
    "return_change_pp": 0.5827,
    "volatility_before": 0.0412,
    "volatility_after": 0.0421,
    "volatility_change_pct": 2.2,
    "credible_interval_lower": "2021-04-30",
    "credible_interval_upper": "2021-04-30",
    "correlated_events": [
        {
            "event_date": "2021-05-01",
            "event_name": "India COVID-19 Second Wave Peaks",
            "event_type": "Economic",
            "days_from_change": 1,
            "direction": "after"
        },
        {
            "event_date": "2021-04-02",
            "event_name": "OPEC+ Gradual Production Increase",
            "event_type": "OPEC Policy",
            "days_from_change": -28,
            "direction": "before"
        },
        {
            "event_date": "2021-03-23",
            "event_name": "Suez Canal Container Ship Blockage",
            "event_type": "Economic",
            "days_from_change": -38,
            "direction": "before"
        }
    ]
}

def get_mock_summary():
    """Generate mock summary statistics based on real analysis."""
    return {
        "latest_price": 93.59,
        "average_price": 68.96,
        "min_price": 52.31,
        "max_price": 143.95,
        "price_range": 91.64,
        "volatility": 0.02553,
        "total_return_pct": 27.6,
        "annualized_return_pct": 8.2,
        "total_events": 10,
        "change_point_date": "2021-04-30",
        "price_impact_pct": 31.8
    }

def get_mock_volatility():
    """Generate mock volatility data."""
    dates = pd.date_range(end=datetime.now(), periods=100, freq='D')
    volatilities = np.random.normal(0.025, 0.005, 100)
    volatilities = np.abs(volatilities)  # Ensure positive
    
    vol_data = []
    for i, date in enumerate(dates):
        vol_data.append({
            "date": date.strftime('%Y-%m-%d'),
            "volatility": round(volatilities[i], 4),
            "price": round(68.96 + np.random.normal(0, 2), 2)
        })
    
    return vol_data