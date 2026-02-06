"""
Pytest fixtures for testing
"""

import pytest
import pandas as pd
import numpy as np


@pytest.fixture
def sample_oil_data():
    """Create sample oil price data for testing."""
    dates = pd.date_range('2020-01-01', periods=200, freq='D')
    
    # Create artificial change point at day 100
    prices = np.concatenate([
        np.random.normal(80, 5, 100),   # Regime 1: ~$80
        np.random.normal(120, 10, 100)  # Regime 2: ~$120
    ])
    
    return pd.DataFrame({
        'Date': dates,
        'Price': prices
    })


@pytest.fixture
def event_catalog():
    """Create sample event catalog."""
    return pd.DataFrame({
        'Date': pd.to_datetime(['2020-03-01', '2021-06-15', '2022-02-24']),
        'Event': ['COVID-19', 'OPEC Meeting', 'Ukraine War'],
        'Impact': ['Negative', 'Positive', 'Positive']
    })
