"""
Bayesian Change Point Detection for Brent Oil Prices
"""

import pandas as pd
import numpy as np
import pymc as pm
import arviz as az
import matplotlib.pyplot as plt
from typing import Tuple, Dict, Optional
import warnings
warnings.filterwarnings('ignore')


class ChangePointDetector:
    """Bayesian change point detection for time series data."""
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize detector with time series data.
        
        Parameters
        ----------
        data : pd.DataFrame
            Must contain 'Date' and 'Price' columns
        """
        self.data = data.copy()
        self.prepare_data()
        self.model = None
        self.trace = None
        
    def prepare_data(self):
        """Prepare data for analysis: convert dates and compute log returns."""
        # Convert date
        self.data['Date'] = pd.to_datetime(self.data['Date'], format='%d-%b-%y')
        self.data = self.data.sort_values('Date').reset_index(drop=True)
        
        # Compute log returns
        self.data['log_return'] = np.log(self.data['Price'] / self.data['Price'].shift(1))
        self.data = self.data.dropna()
        
        # Store returns as numpy array for PyMC
        self.returns = self.data['log_return'].values
        
    def build_single_change_point_model(self):
        """Build Bayesian model with single change point."""
        n_obs = len(self.returns)
        
        with pm.Model() as model:
            # Prior for change point (can be any day except first/last)
            tau = pm.DiscreteUniform("tau", lower=1, upper=n_obs-1)
            
            # Priors for means before and after change
            mu1 = pm.Normal("mu1", mu=0, sigma=1)
            mu2 = pm.Normal("mu2", mu=0, sigma=1)
            
            # Priors for standard deviations (volatility)
            sigma1 = pm.HalfNormal("sigma1", sigma=1)
            sigma2 = pm.HalfNormal("sigma2", sigma=1)
            
            # Switch function: use parameters based on position relative to tau
            mean = pm.math.switch(self.data.index.values < tau, mu1, mu2)
            sigma = pm.math.switch(self.data.index.values < tau, sigma1, sigma2)
            
            # Likelihood (observations)
            likelihood = pm.Normal(
                "returns", 
                mu=mean, 
                sigma=sigma, 
                observed=self.returns
            )
            
        self.model = model
        return model
    
    def sample(self, draws: int = 2000, tune: int = 1000, chains: int = 2):
        """Run MCMC sampling."""
        if self.model is None:
            self.build_single_change_point_model()
        
        with self.model:
            self.trace = pm.sample(
                draws=draws,
                tune=tune,
                chains=chains,
                random_seed=42,
                progressbar=True
            )
        
        return self.trace
    
    def check_convergence(self) -> Dict:
        """Check MCMC convergence diagnostics."""
        if self.trace is None:
            raise ValueError("Must run sampling first")
        
        summary = az.summary(self.trace, round_to=4)
        
        # Check R-hat values
        rhats = summary['r_hat']
        converged = all(rhats < 1.1)
        
        return {
            'converged': converged,
            'summary': summary,
            'max_rhat': rhats.max(),
            'min_rhat': rhats.min()
        }
    
    def get_change_point(self) -> Tuple[pd.Timestamp, float]:
        """Extract most probable change point."""
        if self.trace is None:
            raise ValueError("Must run sampling first")
        
        # Get posterior samples for tau
        tau_samples = self.trace.posterior['tau'].values.flatten()
        
        # Get most probable change point (median)
        tau_median = int(np.median(tau_samples))
        
        # Convert to date
        change_date = self.data.iloc[tau_median]['Date']
        
        # Get credible interval (90%)
        tau_lower = int(np.percentile(tau_samples, 5))
        tau_upper = int(np.percentile(tau_samples, 95))
        date_lower = self.data.iloc[tau_lower]['Date']
        date_upper = self.data.iloc[tau_upper]['Date']
        
        return {
            'date': change_date,
            'index': tau_median,
            'credible_interval': {
                'lower': date_lower,
                'upper': date_upper,
                'lower_idx': tau_lower,
                'upper_idx': tau_upper
            },
            'probability': len(tau_samples[tau_samples == tau_median]) / len(tau_samples)
        }
    
    def plot_results(self, save_path: Optional[str] = None):
        """Plot analysis results."""
        if self.trace is None:
            raise ValueError("Must run sampling first")
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Plot 1: Time series with change point
        ax1 = axes[0, 0]
        ax1.plot(self.data['Date'], self.data['Price'], alpha=0.7)
        
        change_info = self.get_change_point()
        change_date = change_info['date']
        ax1.axvline(change_date, color='red', linestyle='--', 
                   label=f'Change Point: {change_date.date()}')
        ax1.fill_betweenx(
            y=[self.data['Price'].min(), self.data['Price'].max()],
            x1=change_info['credible_interval']['lower'],
            x2=change_info['credible_interval']['upper'],
            alpha=0.3, color='red', label='90% Credible Interval'
        )
        ax1.set_title('Brent Oil Prices with Change Point')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Price (USD)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Posterior distribution of tau
        ax2 = axes[0, 1]
        tau_samples = self.trace.posterior['tau'].values.flatten()
        ax2.hist(tau_samples, bins=50, density=True, alpha=0.7, edgecolor='black')
        ax2.axvline(np.median(tau_samples), color='red', 
                   label=f'Median: {int(np.median(tau_samples))}')
        ax2.set_title('Posterior Distribution of Change Point (τ)')
        ax2.set_xlabel('Time Index')
        ax2.set_ylabel('Density')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Trace plots for key parameters
        ax3 = axes[1, 0]
        mu1_trace = self.trace.posterior['mu1'].values.flatten()
        mu2_trace = self.trace.posterior['mu2'].values.flatten()
        ax3.plot(mu1_trace[:500], alpha=0.7, label='μ1 (before)')
        ax3.plot(mu2_trace[:500], alpha=0.7, label='μ2 (after)')
        ax3.set_title('Trace Plot: μ1 and μ2 (first 500 samples)')
        ax3.set_xlabel('Sample')
        ax3.set_ylabel('Value')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Distribution of means before/after
        ax4 = axes[1, 1]
        ax4.hist(mu1_trace, bins=50, alpha=0.5, label='μ1 (before)', density=True)
        ax4.hist(mu2_trace, bins=50, alpha=0.5, label='μ2 (after)', density=True)
        ax4.axvline(mu1_trace.mean(), color='blue', linestyle='--')
        ax4.axvline(mu2_trace.mean(), color='orange', linestyle='--')
        ax4.set_title('Distribution of Means Before/After Change')
        ax4.set_xlabel('Mean Return')
        ax4.set_ylabel('Density')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
        
        # Print summary statistics
        print("=" * 60)
        print("CHANGE POINT ANALYSIS RESULTS")
        print("=" * 60)
        print(f"Most probable change date: {change_date.date()}")
        print(f"90% Credible Interval: {change_info['credible_interval']['lower'].date()} to {change_info['credible_interval']['upper'].date()}")
        print(f"Probability at this point: {change_info['probability']:.2%}")
        print(f"Mean return before: {mu1_trace.mean():.4f}")
        print(f"Mean return after: {mu2_trace.mean():.4f}")
        print(f"Change in mean: {(mu2_trace.mean() - mu1_trace.mean()):.4f}")
        print(f"Percentage change: {((mu2_trace.mean() - mu1_trace.mean()) / abs(mu1_trace.mean()) * 100):.1f}%")
        print("=" * 60)


def main():
    """Main analysis pipeline."""
    print("Loading data...")
    # Load data - adjust path as needed
    df = pd.read_csv('data/raw/brent_prices.csv')
    
    print("Initializing detector...")
    detector = ChangePointDetector(df)
    
    print("Building model...")
    detector.build_single_change_point_model()
    
    print("Running MCMC sampling...")
    detector.sample(draws=2000, tune=1000, chains=2)
    
    print("Checking convergence...")
    convergence = detector.check_convergence()
    print(f"Converged: {convergence['converged']}")
    print(f"Max R-hat: {convergence['max_rhat']:.4f}")
    
    print("Plotting results...")
    detector.plot_results(save_path='reports/change_point_analysis.png')
    
    return detector


if __name__ == "__main__":
    main()
