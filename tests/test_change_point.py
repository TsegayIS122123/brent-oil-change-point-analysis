"""
Test Change Point Detection
Test-Driven Development (TDD) approach
"""

import pytest
import pandas as pd
import numpy as np
from src.models.change_point import ChangePointDetector


class TestChangePointDetector:
    """Test suite for ChangePointDetector class."""
    
    def test_data_loading(self):
        """Test data loading and preparation."""
        # Arrange
        dates = pd.date_range('2020-01-01', periods=100, freq='D')
        prices = np.random.normal(100, 5, 100)
        df = pd.DataFrame({'Date': dates, 'Price': prices})
        
        # Act
        detector = ChangePointDetector(df)
        
        # Assert
        assert 'log_return' in detector.data.columns
        assert detector.data['Date'].dtype == 'datetime64[ns]'
        assert len(detector.returns) == 99  # One less due to shift
    
    def test_model_building(self):
        """Test Bayesian model construction."""
        # Arrange
        dates = pd.date_range('2020-01-01', periods=50, freq='D')
        prices = np.random.normal(100, 5, 50)
        df = pd.DataFrame({'Date': dates, 'Price': prices})
        detector = ChangePointDetector(df)
        
        # Act
        model = detector.build_single_change_point_model()
        
        # Assert
        assert model is not None
        assert 'tau' in model.named_vars
        assert 'mu1' in model.named_vars
        assert 'mu2' in model.named_vars
    
    def test_log_returns_calculation(self):
        """Test log returns are calculated correctly."""
        # Arrange
        dates = pd.date_range('2020-01-01', periods=3, freq='D')
        prices = [100, 110, 121]  # 10% increase each day
        df = pd.DataFrame({'Date': dates, 'Price': prices})
        
        # Act
        detector = ChangePointDetector(df)
        
        # Assert
        expected_returns = np.log(np.array([110/100, 121/110]))
        np.testing.assert_array_almost_equal(
            detector.returns, 
            expected_returns,
            decimal=5
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
