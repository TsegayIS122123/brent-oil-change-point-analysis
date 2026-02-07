# Brent Oil Price Change Point Analysis Plan
**Birhan Energies - Strategic Insights Division**
*Date: February 7, 2026*
*Author: Tsegay, Data Scientist*

## 1. Executive Summary
This document outlines the comprehensive analysis plan for investigating the impact of geopolitical and economic events on Brent crude oil prices using Bayesian change point detection. The analysis aims to identify structural breaks in oil price time series and quantify event impacts to support investment decisions, policy formulation, and operational planning.

## 2. Analysis Workflow

### Phase 1: Data Preparation & Exploratory Analysis (Days 1-2)
**Objective**: Understand data characteristics and prepare for modeling

1. **Data Loading & Cleaning**
   - Load historical Brent oil prices (1987-2022)
   - Handle missing values and outliers
   - Convert date formats and ensure chronological order
   - Validate data integrity and completeness

2. **Event Data Compilation**
   - Research 15+ key geopolitical/economic events (1990-2022)
   - Create structured event database with dates, types, descriptions
   - Classify events by type (Geopolitical, OPEC Policy, Economic Sanctions)
   - Assign severity ratings (Low, Medium, High, Very High)

3. **Exploratory Data Analysis**
   - Visualize price trends over time
   - Calculate descriptive statistics
   - Analyze distribution properties
   - Identify periods of high volatility

### Phase 2: Statistical Pre-Modeling Analysis (Day 3)
**Objective**: Assess time series properties to inform modeling choices

1. **Stationarity Testing**
   - Augmented Dickey-Fuller test on raw prices
   - Test on log returns for stationarity
   - Determine differencing requirements

2. **Volatility Analysis**
   - Calculate rolling standard deviations
   - Identify volatility clustering patterns
   - Test for ARCH/GARCH effects

3. **Decomposition Analysis**
   - Separate trend, seasonal, and residual components
   - Assess autocorrelation patterns
   - Identify structural breaks visually

### Phase 3: Bayesian Change Point Modeling (Days 4-5)
**Objective**: Detect structural breaks using Bayesian inference

1. **Model Specification**
   - Define priors for change point location (τ)
   - Specify before/after regime parameters (μ₁, μ₂, σ)
   - Implement likelihood function using switch mechanism
   - Consider multiple change point extensions

2. **Model Estimation**
   - Run MCMC sampling (NUTS algorithm)
   - Use 4 chains with 2000 samples each
   - Include 1000 tuning samples per chain

3. **Convergence Diagnostics**
   - Check R-hat statistics (< 1.01)
   - Examine trace plots for mixing
   - Assess effective sample sizes
   - Validate posterior predictive checks

### Phase 4: Event Correlation & Impact Quantification (Day 6)
**Objective**: Link statistical findings with real-world events

1. **Change Point Interpretation**
   - Convert τ indices to calendar dates
   - Calculate 95% credible intervals
   - Identify most probable change points

2. **Event Matching**
   - Map change points to nearby events (±30 days)
   - Consider event severity and type
   - Account for market anticipation effects

3. **Impact Measurement**
   - Calculate pre/post price differences
   - Compute percentage changes
   - Measure volatility shifts
   - Perform statistical significance tests

### Phase 5: Insight Generation & Reporting (Day 7)
**Objective**: Transform analysis into actionable insights

1. **Stakeholder-Specific Recommendations**
   - Investor guidance: Risk management strategies
   - Policy implications: Economic stability measures
   - Corporate insights: Operational planning adjustments

2. **Visualization Development**
   - Create time series plots with change points
   - Design event impact charts
   - Build correlation matrices

3. **Reporting & Dashboard Development**
   - Generate technical report
   - Create executive summary
   - Develop interactive dashboard

## 3. Assumptions & Limitations

### Critical Assumptions

1. **Structural Break Assumption**: The oil price series can be modeled as having distinct regimes with different statistical properties.

2. **Event Impact Timing**: Market reactions to major events occur within a reasonable timeframe (typically 0-30 days).

3. **Ceteris Paribus Condition**: When analyzing specific events, we assume other factors remain relatively constant.

4. **Model Specification**: The normal distribution adequately represents price variations within regimes.

5. **Information Efficiency**: Markets quickly incorporate new information into prices.

### Important Limitations

1. **Correlation vs. Causation**
   - **Critical Distinction**: Identifying a change point coinciding with an event demonstrates statistical correlation in time but does not prove causal impact.
   - **Confounding Factors**: Multiple simultaneous events can create attribution challenges.
   - **Market Anticipation**: Prices may adjust before official event dates due to rumors or expectations.
   - **Reverse Causality**: Oil price changes can themselves trigger geopolitical responses.

2. **Data Limitations**
   - Daily frequency may miss intraday reactions
   - Limited to Brent crude (other benchmarks may differ)
   - Historical data may not reflect future market structures

3. **Model Limitations**
   - Single change point model oversimplifies complex dynamics
   - Assumes constant variance within regimes
   - Doesn't incorporate external economic indicators

4. **Event Measurement**
   - Event severity classification is subjective
   - Exact timing of market impact is uncertain
   - Global events have heterogeneous regional impacts

## 4. Communication Strategy

### Target Audiences & Channels

| Stakeholder Group | Primary Channel | Secondary Channel | Key Message Focus |
|------------------|----------------|-------------------|-------------------|
| **Investors** | Interactive Dashboard | Executive Briefing | Risk timing, hedging strategies, regime shift indicators |
| **Policymakers** | Policy Brief (PDF) | Presentation | Economic stability, strategic reserves, energy security |
| **Energy Companies** | Technical Report | Workshop | Operational planning, cost management, supply chain risks |
| **Analysts** | Jupyter Notebook | API Access | Methodology, statistical outputs, model specifications |

### Deliverable Formats

1. **Interactive Dashboard** (React/Flask)
   - Real-time visualization of change points
   - Event impact explorer
   - Custom filtering and date range selection
   - Export functionality for reports

2. **Technical Report** (PDF/Markdown)
   - Complete methodology documentation
   - Statistical results with uncertainty quantification
   - Model validation and diagnostics
   - Code repository links

3. **Executive Summary** (2-page PDF)
   - Key findings in non-technical language
   - Actionable recommendations
   - Visual highlights of major insights

4. **API Endpoints** (RESTful)
   - Programmatic access to analysis results
   - Event correlation data
   - Model predictions and simulations

### Communication Timeline
- **Day 3**: Preliminary findings shared with core team
- **Day 5**: Model validation results presented
- **Day 7**: Final deliverables distributed to all stakeholders
- **Day 8**: Q&A session and implementation guidance