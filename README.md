# 📈 Pairs Trading Statistical Arbitrage Project

This project implements and evaluates a **statistical arbitrage strategy** using **pairs trading**. The goal is to identify pairs of historically correlated stocks whose prices tend to revert to a mean relationship. When their prices diverge beyond a threshold, the strategy exploits this deviation with a long-short trade in anticipation of mean reversion.

---

## 🧠 Key Concepts

- **Mean Reversion**: The tendency of a spread between two related assets to return to its historical average.
- **Statistical Arbitrage**: A trading strategy that uses statistical methods to exploit pricing inefficiencies.
- **Cointegration**: A statistical property indicating a long-term equilibrium relationship between two time series.
- **Z-score**: A normalized metric indicating how far a value is from the mean, used to trigger trades.

---

## 🧱 Project Structure

pairs_trading_project/
├── data/ # Raw and processed stock price data
├── notebooks/ # EDA and experimentation in Jupyter Notebooks
├── results/ # Backtest results, plots, metrics
├── scripts/ # Finalized, runnable scripts
├── src/ # Core source code (functions, models, strategy)
├── .gitignore # Files/folders to ignore in version control
├── README.md # Project overview and guide
└── requirements.txt# List of dependencies

---

## 🚶 Step-by-Step Workflow

### 1. 📥 Data Acquisition
- Use `yfinance` or a similar API to download historical stock prices.
- Save the data as `.csv` in the `/data/` folder.

### 2. 📊 Exploratory Data Analysis (EDA)
- Analyze price movements, correlations, and visual patterns.
- Compute:
  - Price ratios
  - Correlation matrices
  - Stationarity via ADF test

### 3. 🔗 Pair Selection
- Identify stock pairs with:
  - High correlation
  - Evidence of cointegration (Engle-Granger or Johansen test)

### 4. 📐 Strategy Design
- Construct the **spread** (price difference or ratio).
- Normalize using a **z-score**.
- Define entry/exit rules:
  - **Enter Long**: z-score < -threshold
  - **Enter Short**: z-score > threshold
  - **Exit**: z-score returns to 0

### 5. 💻 Backtesting
- Simulate trades over historical data.
- Track:
  - Portfolio value
  - Trade log
  - Position sizes
  - Transaction costs (if any)

### 6. 📈 Performance Evaluation
- Key metrics:
  - Sharpe Ratio
  - Win Ratio
  - Cumulative Returns
  - Maximum Drawdown
  - Number of Trades

### 7. 📊 Result Visualization
- Plot:
  - Cumulative returns (equity curve)
  - Z-score vs. trade signals
  - Spread over time with thresholds

### 8. 🔁 Strategy Extension (Optional)
- Automate pair selection across a sector.
- Add more pairs or construct baskets.
- Optimize thresholds or incorporate machine learning.

---

## 🧠 Skills & Tools

- Python (NumPy, Pandas, Matplotlib, Statsmodels, Scikit-learn)
- Time series analysis
- Data wrangling and visualization
- Quantitative strategy development
- Backtesting methodology
- Git and GitHub for version control

---

## 🚀 Goal

Build a fully functional pairs trading pipeline with potential to expand into sector-level arbitrage, baskets, or real-time signal generation.

---

## 📌 Status

🚧 **Project in progress**  
✅ Next step: EDA and pair selection in `/notebooks/`

---
