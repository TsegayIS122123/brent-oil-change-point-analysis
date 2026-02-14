"""
Unit tests for change point model.
Run with: pytest tests/test_change_point.py -v
"""
import pytest
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.change_point_model import ChangePointModel, ModelConfig


class TestChangePointModel:
    """Test suite for ChangePointModel class."""
    
    @pytest.fixture
    def sample_returns(self):
        """Create sample return data with a clear change point."""
        np.random.seed(42)
        # Before change: slightly negative returns
        before = np.random.normal(-0.001, 0.02, 50)
        # After change: slightly positive returns
        after = np.random.normal(0.002, 0.02, 50)
        return np.concatenate([before, after])
    
    @pytest.fixture
    def sample_price_data(self):
        """Create sample price data with a change point."""
        dates = pd.date_range(start='2020-01-01', periods=200, freq='D')
        # Before: stable around 50
        before_prices = 50 + np.cumsum(np.random.randn(100) * 0.1)
        # After: higher around 60
        after_prices = 60 + np.cumsum(np.random.randn(100) * 0.1)
        prices = np.concatenate([before_prices, after_prices])
        
        return pd.DataFrame({
            'Date': dates,
            'Price': prices,
            'Log_Return': np.log(prices / np.roll(prices, 1))
        })
    
    def test_1_initialization(self):
        """Test model initialization with custom config."""
        config = ModelConfig(
            n_chains=1,
            n_samples=100,
            n_tuning=50,
            cores=1,
            use_student_t=False
        )
        model = ChangePointModel(config)
        
        assert model.config.n_chains == 1
        assert model.config.n_samples == 100
        assert model.config.n_tuning == 50
        assert model.config.cores == 1
        assert model.config.use_student_t is False
        assert model.model is None
        assert model.trace is None
        print("✓ test_1_initialization passed")
    
    def test_2_build_model(self, sample_returns):
        """Test model building without fitting."""
        model = ChangePointModel()
        model.build_single_change_point_model(sample_returns)
        
        assert model.model is not None
        assert hasattr(model.model, 'basic_RVs')
        print("✓ test_2_build_model passed")
    
    def test_3_fit_small_data(self):
        """Test fitting with small dataset (fast)."""
        # Create tiny dataset for quick test
        data = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.4, 0.3, 0.2, 0.1])
        
        config = ModelConfig(
            n_chains=1,
            n_samples=100,
            n_tuning=25,
            cores=1,
            use_student_t=False
        )
        
        model = ChangePointModel(config)
        model.fit(data)
        
        assert model.trace is not None
        assert model.change_point_idx is not None
        assert model.change_point_idx >= 0
        assert model.change_point_idx < len(data)
        print("✓ test_3_fit_small_data passed")
    
    def test_4_get_summary(self, sample_returns):
        """Test summary generation after fitting."""
        config = ModelConfig(
            n_chains=1,
            n_samples=100,
            n_tuning=25,
            cores=1,
            use_student_t=False
        )
        model = ChangePointModel(config)
        model.fit(sample_returns)
        
        summary = model.get_change_point_summary()
        
        assert 'change_point_idx' in summary
        assert 'probability' in summary
        assert 'mu_before_mean' in summary
        assert 'mu_after_mean' in summary
        assert 'mu_difference' in summary
        assert 'rhat_values' in summary
        
        # Check that probability is between 0 and 1
        assert 0 <= summary['probability'] <= 1
        print("✓ test_4_get_summary passed")
    
    def test_5_calculate_price_impact(self, sample_price_data):
        """Test price impact calculation."""
        model = ChangePointModel()
        
        # Set a known change point at index 100
        model.change_point_idx = 100
        
        impact = model.calculate_price_impact(sample_price_data)
        
        assert 'price_before' in impact
        assert 'price_after' in impact
        assert 'price_change_abs' in impact
        assert 'price_change_pct' in impact
        assert 'volatility_before' in impact
        assert 'volatility_after' in impact
        assert 'n_before' in impact
        assert 'n_after' in impact
        
        # Check that counts match
        assert impact['n_before'] == 100
        assert impact['n_after'] == 100
        print("✓ test_5_calculate_price_impact passed")
    
    def test_6_error_handling(self):
        """Test error handling when calling methods before fitting."""
        model = ChangePointModel()
        
        with pytest.raises(ValueError) as exc_info:
            model.get_change_point_summary()
        assert "Model not fitted" in str(exc_info.value)
        
        with pytest.raises(ValueError) as exc_info:
            model.calculate_price_impact(pd.DataFrame())
        assert "Change point not identified" in str(exc_info.value)
        print("✓ test_6_error_handling passed")
    
    def test_7_config_validation(self):
        """Test config validation."""
        # Invalid n_chains
        with pytest.raises(ValueError):
            ModelConfig(n_chains=0)
        
        # Invalid n_samples
        with pytest.raises(ValueError):
            ModelConfig(n_samples=50)  # Less than 100
        
        print("✓ test_7_config_validation passed")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])