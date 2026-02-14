"""
Bayesian change point detection for time series data.
Uses PyMC for MCMC sampling to detect structural breaks.
FIXED: Added freeze_support() protection for Windows multiprocessing
"""
from typing import Tuple, Optional, Dict, Any, List
import numpy as np
import pandas as pd
import pymc as pm
import arviz as az
from dataclasses import dataclass, field
import multiprocessing as mp

# Critical for Windows - must be at module level
if __name__ == '__main__':
    mp.freeze_support()


@dataclass
class ModelConfig:
    """Configuration for Bayesian change point model."""
    
    # Model parameters
    n_chains: int = 2  # Reduced from 4 for Windows compatibility
    n_samples: int = 1000  # Reduced from 2000 for speed
    n_tuning: int = 500  # Reduced from 1000
    target_accept: float = 0.95
    random_seed: int = 42
    
    # Prior parameters
    mu_prior_mean: float = 0.0
    mu_prior_sigma: float = 0.1
    sigma_prior_sigma: float = 0.1
    
    # Model type
    use_student_t: bool = True  # Use t-distribution for fat tails
    multiple_change_points: bool = False
    max_change_points: int = 5
    
    # Sampling mode - CRITICAL for Windows
    cores: int = 1  # Use single core to avoid multiprocessing issues
    progressbar: bool = True
    
    def __post_init__(self):
        """Validate configuration."""
        if self.n_chains < 1:
            raise ValueError("n_chains must be >= 1")
        if self.n_samples < 100:
            raise ValueError("n_samples must be >= 100")


class ChangePointModel:
    """Bayesian change point detection model."""
    
    def __init__(self, config: Optional[ModelConfig] = None):
        """
        Initialize change point model.
        
        Args:
            config: ModelConfig object with parameters
        """
        self.config = config or ModelConfig()
        self.model: Optional[pm.Model] = None
        self.trace: Optional[az.InferenceData] = None
        self.summary: Optional[pd.DataFrame] = None
        self.change_point_idx: Optional[int] = None
        self.change_point_date: Optional[str] = None
        
    def build_single_change_point_model(
        self, 
        data: np.ndarray, 
        dates: Optional[List[str]] = None
    ) -> pm.Model:
        """
        Build PyMC model for single change point detection.
        
        Args:
            data: Time series data (log returns)
            dates: Optional list of dates for indexing
            
        Returns:
            PyMC model
        """
        n_obs = len(data)
        
        with pm.Model() as model:
            # Prior for change point location
            tau = pm.DiscreteUniform('tau', lower=0, upper=n_obs-1)
            
            # Priors for mean before and after
            mu_before = pm.Normal(
                'mu_before', 
                mu=self.config.mu_prior_mean, 
                sigma=self.config.mu_prior_sigma
            )
            mu_after = pm.Normal(
                'mu_after', 
                mu=self.config.mu_prior_mean, 
                sigma=self.config.mu_prior_sigma
            )
            
            # Prior for standard deviation
            sigma = pm.HalfNormal(
                'sigma', 
                sigma=self.config.sigma_prior_sigma
            )
            
            # Switch function: select appropriate mean based on tau
            mu = pm.math.switch(tau >= np.arange(n_obs), mu_before, mu_after)
            
            # Likelihood
            if self.config.use_student_t:
                # Student's t-distribution for fat tails
                nu = pm.Exponential('nu', lam=1/10)
                likelihood = pm.StudentT(
                    'returns', 
                    mu=mu, 
                    sigma=sigma, 
                    nu=nu,
                    observed=data
                )
            else:
                # Normal distribution (simpler)
                likelihood = pm.Normal(
                    'returns', 
                    mu=mu, 
                    sigma=sigma, 
                    observed=data
                )
                
        self.model = model
        return model
    
    def fit(self, data: np.ndarray, dates: Optional[List[str]] = None) -> az.InferenceData:
        """
        Fit the change point model using MCMC.
        
        Args:
            data: Time series data
            dates: Optional dates for reference
            
        Returns:
            ArviZ InferenceData object with trace
        """
        if self.model is None:
            self.build_single_change_point_model(data, dates)
            
        with self.model:
            self.trace = pm.sample(
                draws=self.config.n_samples,
                tune=self.config.n_tuning,
                chains=self.config.n_chains,
                cores=self.config.cores,  # Use single core
                target_accept=self.config.target_accept,
                random_seed=self.config.random_seed,
                return_inferencedata=True,
                progressbar=self.config.progressbar
            )
            
        self.summary = az.summary(self.trace)
        
        # Extract most likely change point
        tau_samples = self.trace.posterior['tau'].values.flatten()
        tau_values, counts = np.unique(tau_samples, return_counts=True)
        self.change_point_idx = int(tau_values[np.argmax(counts)])
        
        if dates:
            self.change_point_date = dates[self.change_point_idx]
            
        return self.trace
    
    def get_change_point_summary(self) -> Dict[str, Any]:
        """
        Get summary of detected change point.
        
        Returns:
            Dictionary with change point information
        """
        if self.trace is None:
            raise ValueError("Model not fitted. Call fit() first.")
            
        # Extract posterior samples
        tau_samples = self.trace.posterior['tau'].values.flatten()
        mu_before_samples = self.trace.posterior['mu_before'].values.flatten()
        mu_after_samples = self.trace.posterior['mu_after'].values.flatten()
        
        # Calculate statistics
        tau_values, tau_counts = np.unique(tau_samples, return_counts=True)
        tau_probs = tau_counts / len(tau_samples)
        max_prob_idx = np.argmax(tau_probs)
        
        return {
            'change_point_idx': int(tau_values[max_prob_idx]),
            'change_point_date': self.change_point_date,
            'probability': float(tau_probs[max_prob_idx]),
            'mu_before_mean': float(np.mean(mu_before_samples)),
            'mu_before_std': float(np.std(mu_before_samples)),
            'mu_after_mean': float(np.mean(mu_after_samples)),
            'mu_after_std': float(np.std(mu_after_samples)),
            'mu_difference': float(np.mean(mu_after_samples) - np.mean(mu_before_samples)),
            'rhat_values': {
                param: float(self.summary.loc[param, 'r_hat'])
                for param in ['tau', 'mu_before', 'mu_after'] if param in self.summary.index
            }
        }
    
    def calculate_price_impact(
        self, 
        price_data: pd.DataFrame,
        price_col: str = 'Price'
    ) -> Dict[str, float]:
        """
        Calculate actual price impact before/after change point.
        
        Args:
            price_data: DataFrame with price data
            price_col: Name of price column
            
        Returns:
            Dictionary with price impact metrics
        """
        if self.change_point_idx is None:
            raise ValueError("Change point not identified. Call fit() first.")
            
        # Split data at change point
        before = price_data.iloc[:self.change_point_idx].copy()
        after = price_data.iloc[self.change_point_idx:].copy()
        
        # Calculate statistics
        before_price = before[price_col].mean() if len(before) > 0 else price_data[price_col].iloc[0]
        after_price = after[price_col].mean() if len(after) > 0 else price_data[price_col].iloc[-1]
        
        price_change = after_price - before_price
        price_change_pct = (price_change / before_price) * 100 if before_price > 0 else 0
        
        before_vol = before[price_col].std() if len(before) > 1 else 0
        after_vol = after[price_col].std() if len(after) > 1 else 0
        vol_change = ((after_vol - before_vol) / before_vol * 100) if before_vol > 0 else 0
        
        return {
            'price_before': float(before_price),
            'price_after': float(after_price),
            'price_change_abs': float(price_change),
            'price_change_pct': float(price_change_pct),
            'volatility_before': float(before_vol),
            'volatility_after': float(after_vol),
            'volatility_change_pct': float(vol_change),
            'n_before': int(len(before)),
            'n_after': int(len(after))
        }