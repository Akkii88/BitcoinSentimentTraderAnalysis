# Market Sentiment vs Trader Performance: Bitcoin Fear & Greed Analysis

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Pandas](https://img.shields.io/badge/Pandas-1.3+-orange.svg)](https://pandas.pydata.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.5+-green.svg)](https://matplotlib.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Executive Summary
Analysis of 211K+ Hyperliquid trades merged with Fear & Greed Index data. Quantifies sentiment's impact on performance, revealing behavioral patterns and asymmetric risks. Delivers rule-based trading system and backtested strategies for risk reduction.

> This project focuses on controlling trader behavior under different sentiment regimes rather than predicting market direction.

## Key Insight
Higher trading activity during Greed phases does not translate into better performance. While win rates increase slightly, losses grow disproportionately larger, indicating that risk asymmetry—not win frequency—drives overall outcomes.

Neutral sentiment provides the most stable environment, with balanced win rates and controlled losses.

## Trading System Logic
Rule-based engine adjusts parameters by sentiment:
- **Extreme Fear**: trade_allowed=False, position_size_factor=0.2, leverage_limit=1.0, stop_loss=2%.
- **Fear**: trade_allowed=True, position_size_factor=0.5, leverage_limit=2.0, stop_loss=3%.
- **Neutral**: trade_allowed=True, position_size_factor=1.0, leverage_limit=3.0, stop_loss=5%.
- **Greed**: trade_allowed=True, position_size_factor=0.3, leverage_limit=1.5, stop_loss=4%.
- **Extreme Greed**: trade_allowed=False, position_size_factor=0.1, leverage_limit=1.0, stop_loss=2.5%.

## Backtest Results
| Metric             | Baseline      | Strategy      |
|--------------------|---------------|---------------|
| Total PnL         | 10,296,959    | 4,483,235     |
| Avg PnL per Trade | 48.75         | 22.05         |
| Win Rate          | 0.411         | 0.409         |
| Max Drawdown      | -443,038      | -221,519      |

The strategy reduces maximum drawdown significantly, at the cost of lower overall returns. This highlights a key trade-off: sentiment-based controls improve risk stability rather than maximizing raw profitability.

## Key Findings
- Trading volume increases significantly during Greed phases, but average performance per trade declines.
- Extreme Greed shows higher win rates (~55%) but also much larger losses (~$463), indicating poor risk control.
- Fear conditions produce fewer trades but more selective positioning, resulting in relatively stable returns.
- Neutral sentiment provides the most consistent performance with balanced risk and reward.
- Extreme Fear leads to reduced participation, limiting both losses and opportunities.
- Loss magnitude is substantially higher in Greed compared to Neutral conditions, highlighting asymmetric risk exposure.
- Position sizing appears more effective in Fear conditions, while over-sizing in Greed reduces efficiency.

## Strategy Recommendations
- Reduce position size and leverage during Greed and Extreme Greed conditions.
- Use sentiment as a risk-control filter rather than a directional signal.
- Limit trade frequency during high-activity (Greed) phases to avoid overtrading.
- Maintain consistent execution strategies during Neutral conditions.
- Apply stricter stop-loss controls in sentiment extremes.

## Industry Impact
- Enables trading systems to adjust risk dynamically based on sentiment regimes.
- Helps reduce exposure to large losses during euphoric market conditions.
- Provides a framework for integrating behavioral signals into execution strategies.
- Supports more consistent performance by controlling sentiment-driven biases.

## System Architecture
1. **Data Ingestion**: Stream trader/sentiment data via Kafka; store in S3/PostgreSQL.
2. **Data Processing**: Clean/standardize with Pandas; compute features.
3. **Sentiment Merging**: Join on dates; add lags.
4. **Rule Engine**: Apply sentiment rules via microservice.
5. **Output Layer**: Generate signals; integrate via APIs.

## Future Work
- Real-time sentiment APIs.
- ML models for prediction.
- Multi-asset expansion.
- Historical backtests.

## How to Run
1. Install: `pip install -r requirements.txt`
2. Run: `python src/assignment_analysis.py`
3. View: `outputs/` (charts), `insights_summary.md`
