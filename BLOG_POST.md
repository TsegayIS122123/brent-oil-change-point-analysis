# Detecting Oil Market Regime Shifts with Bayesian Change Point Analysis

*How I used PyMC and Bayesian statistics to quantify the impact of geopolitical events on Brent crude oil prices*

**By Tsegay Assefa** | February 2026

---

## 🎯 The Business Problem

Brent crude oil is a global economic benchmark, yet its price is constantly disrupted by OPEC decisions, international sanctions, and geopolitical conflicts. Investment firms and energy companies lose millions of dollars annually because they cannot distinguish temporary market noise from permanent structural shifts.

When a major event occurs—like the Russia-Ukraine conflict or OPEC+ production cuts—traders need to know: *"Is this a 1-week blip or a 6-month regime change?"* Policymakers need evidence to evaluate whether sanctions or strategic reserve releases actually work. Energy companies make billion-dollar inventory decisions without quantifying regime change risk.

This project provides a data-driven Bayesian framework that detects exactly when the market "breaks" and quantifies exactly how much each major event actually changes prices.

---

## 📊 The Data

I analyzed **35 years of daily Brent oil prices** from May 20, 1987 to November 14, 2022:

- **9,011 daily observations**
- **Price range:** $9.10 to $143.95 per barrel
- **Average price:** $48.42 per barrel
- **Annualized volatility:** 40.53% (extremely high)

I also curated **18 major geopolitical and economic events** with their dates, types, and severity levels:

| Event | Date | Type | Severity |
|-------|------|------|----------|
| Iraq invades Kuwait | 1990-08-02 | Geopolitical Conflict | Very High |
| 9/11 Attacks | 2001-09-11 | Geopolitical | Very High |
| Global Financial Crisis | 2008-07-11 | Economic | Very High |
| COVID-19 Pandemic | 2020-01-02 | Economic | Very High |
| Russia invades Ukraine | 2022-02-24 | Geopolitical Conflict | Very High |

---

## 🔬 Statistical Analysis

Before building the model, I conducted rigorous statistical analysis to understand the data's properties:

| Test | Result | Interpretation |
|------|--------|----------------|
| ADF Test (Raw Prices) | p=0.289 | Non-stationary ❌ |
| ADF Test (Log Returns) | p=0.000 | Stationary ✅ |
| Jarque-Bera Test | p=0.000 | Fat tails confirmed |
| ARCH Test | p=0.000 | Volatility clustering |
| Skewness | -1.744 | More large drops than jumps |
| Kurtosis | 65.905 | Extreme fat tails |

**Critical Insight:** Oil returns are stationary but highly non-normal, requiring robust statistical methods (Student's t-distribution) rather than simple Normal models.

---

## 🧠 Bayesian Change Point Model

I implemented a Bayesian change point model using PyMC with the following specification:

```python
with pm.Model() as model:
    # Change point location (uniform prior)
    tau = pm.DiscreteUniform('tau', lower=0, upper=n_obs-1)
    
    # Mean parameters before and after
    mu_before = pm.Normal('mu_before', mu=0, sigma=0.1)
    mu_after = pm.Normal('mu_after', mu=0, sigma=0.1)
    
    # Volatility
    sigma = pm.HalfNormal('sigma', sigma=0.1)
    
    # Switch function
    mu = pm.math.switch(tau >= np.arange(n_obs), mu_before, mu_after)
    
    # Likelihood (Student's t for fat tails)
    nu = pm.Exponential('nu', lam=1/10)
    likelihood = pm.StudentT('returns', mu=mu, sigma=sigma, nu=nu, observed=data)
    ```
🎯 Key Findings
Structural Break Detected: April 30, 2021
Statistical Confidence: 99.47% posterior probability

95% Credible Interval: April 30, 2021 (high certainty)

Quantified Impact:
Metric	Before Change	After Change	Change
Average Price	$52.31/barrel	$68.96/barrel	+$16.65 (+31.8%)
Daily Returns	-0.1790%	+0.4043%	+0.5827 pp
Annualized Returns	-36.5%	+174.3%	+146.8 pp
Volatility	0.0412	0.0421	+2.2%
Event Correlation:
Three major events occurred within ±45 days of the change point:

Event Date	Days from Change	Event	Type
2021-05-01	+1 day (after)	India COVID-19 Second Wave Peaks	Economic
2021-04-02	-28 days (before)	OPEC+ Gradual Production Increase	OPEC Policy
2021-03-23	-38 days (before)	Suez Canal Container Ship Blockage	Economic
Interpretation: The change point correlates strongly with the India COVID wave peak and OPEC+ policy shift, suggesting market reaction to demand concerns and supply adjustments.

💼 Business Impact
For Investors:
$16.65/barrel opportunity identified – portfolio rebalancing around April-May 2021 would have captured significant gains

Risk management: Volatility increased by 2.2%, requiring updated hedging strategies

Regime shift detection: Market moved from bearish (-0.18% daily) to bullish (+0.40% daily)

For Policymakers:
Energy security: Demand shocks (like India COVID wave) trigger structural market changes

Policy evaluation: OPEC+ production cuts showed measurable impact within 28 days

Early warning: Change points can signal market stress requiring preemptive measures

For Energy Companies:
Supply chain: $16.65/barrel price increase requires procurement strategy adjustment

Hedging: Increased volatility signals need for derivative positioning

Planning: Incorporate regime-aware forecasting into budgeting

🏗️ Technical Implementation
I built a production-ready full-stack application to deliver these insights:

Backend (Flask)
RESTful API with 8 endpoints serving real data

9,011 price records + 18 events loaded dynamically

Type hints, dataclasses, and modular code structure

Unit tests with 80%+ coverage

Frontend (React)
Interactive dashboard with 4 tabs (Overview, Analytics, Predictions, Events)

Real-time price visualization with event markers

Bayesian change point results (99.5% confidence)

Event impact analysis with before/after comparisons

Responsive design for desktop, tablet, and mobile

DevOps
GitHub Actions CI/CD pipeline with automated testing

Docker containerization for reproducible deployment

Deployed on Vercel (frontend) and Render (backend)

📊 Dashboard Preview
[Insert your dashboard screenshots here]

The dashboard allows stakeholders to:

Explore 35 years of price history with interactive filtering

See detected change points with confidence intervals

Correlate events with price movements

Understand business impact in plain language

⚠️ Limitations & Future Work
Limitations:
Single change point only – 35 years likely contains multiple regime shifts

Correlation ≠ Causation – Statistical association doesn't prove causal impact

Confounding events – Multiple simultaneous events create attribution challenges

Market anticipation – Prices may adjust before official event dates

Future Improvements:
Multiple change point detection using Bayesian non-parametric methods

SHAP explainability to identify which features drive predictions

Real-time data pipeline for live monitoring

Additional data sources (GDP, inflation, exchange rates)

GARCH components to better model volatility clustering

🛠️ Code & Resources
GitHub Repository: https://github.com/TsegayIS122123/brent-oil-change-point-analysis

Live Dashboard: https://brent-oil-change-point-analysis-3qmaov6iq.vercel.app

API Endpoint: https://brent-oil-api.onrender.com

🙏 Acknowledgments
Special thanks to my tutors at 10 Academy – Kerod, Filimon, and Mahbubah – for their guidance throughout this project. Thanks also to the PyMC team for their excellent Bayesian modeling tools and the React community for comprehensive frontend libraries.

📬 Contact
Tsegay Assefa
Email: tsegayassefa27@gmail.com
LinkedIn: linkedin.com/in/tsegay-assefa-95a397336
GitHub: github.com/TsegayIS122123    