"""
Data models and schemas for Brent Oil analysis.
Used for type validation and data consistency.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
import pandas as pd

@dataclass
class PriceData:
    """Model for historical price data."""
    date: datetime
    price: float
    log_return: Optional[float] = None
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create from dictionary."""
        return cls(
            date=pd.to_datetime(data['Date']),
            price=float(data['Price']),
            log_return=float(data.get('Log_Return', 0))
        )

@dataclass
class EventData:
    """Model for geopolitical/economic events."""
    event_date: datetime
    event_name: str
    event_type: str
    severity: str
    region: str = "Global"
    description: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create from dictionary."""
        return cls(
            event_date=pd.to_datetime(data['event_date']),
            event_name=data['event_name'],
            event_type=data['event_type'],
            severity=data.get('severity', 'Medium'),
            region=data.get('region', 'Global'),
            description=data.get('description')
        )

@dataclass
class ChangePointResult:
    """Model for change point analysis results."""
    change_point_date: datetime
    price_before: float
    price_after: float
    price_change_pct: float
    credible_interval_lower: datetime
    credible_interval_upper: datetime
    correlated_events: List[dict]
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create from dictionary."""
        return cls(
            change_point_date=pd.to_datetime(data['change_point_date']),
            price_before=float(data['price_before']),
            price_after=float(data['price_after']),
            price_change_pct=float(data['price_change_pct']),
            credible_interval_lower=pd.to_datetime(data['credible_interval_lower']),
            credible_interval_upper=pd.to_datetime(data['credible_interval_upper']),
            correlated_events=data.get('correlated_events', [])
        )

@dataclass
class SummaryStats:
    """Model for summary statistics."""
    latest_price: float
    average_price: float
    min_price: float
    max_price: float
    volatility: float
    total_events: int
    annualized_return_pct: float
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create from dictionary."""
        return cls(
            latest_price=float(data['latest_price']),
            average_price=float(data['average_price']),
            min_price=float(data['min_price']),
            max_price=float(data['max_price']),
            volatility=float(data['volatility']),
            total_events=int(data['total_events']),
            annualized_return_pct=float(data['annualized_return_pct'])
        )