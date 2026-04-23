# Market Sentiment vs Trader Performance: Bitcoin Fear & Greed Analysis

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Pandas](https://img.shields.io/badge/Pandas-1.3+-orange.svg)](https://pandas.pydata.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.5+-green.svg)](https://matplotlib.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 Key Insight

Greed increases trading activity but concentrates downside risk through larger losses and weaker risk control.

🔥 HEADER (ADD THIS UNDER TITLE)
> This project focuses on controlling trader behavior under different sentiment regimes rather than predicting market direction.
✅ EXECUTIVE SUMMARY (REFINED)
## Executive Summary

This project analyzes 211K+ crypto trades alongside Bitcoin Fear & Greed sentiment data to understand how market psychology impacts trader performance.

The analysis reveals that sentiment significantly influences trading behavior, particularly in terms of risk-taking, trade frequency, and loss magnitude.

A rule-based system is developed to adjust trading behavior dynamically across sentiment regimes, improving risk stability and reducing exposure to large losses.

This shows that managing trader behavior is often more impactful than predicting market direction.
✅ KEY INSIGHT (ELITE VERSION)
## Key Insight

Higher trading activity during Greed phases does not translate into better performance. While win rates increase slightly, losses increase disproportionately relative to gains, indicating that risk asymmetry—not win frequency—drives outcomes.

Neutral sentiment provides the most stable environment, with balanced returns and controlled downside risk.
✅ TRADING SYSTEM LOGIC (KEEP BUT CLEAN)
## Trading System Logic

A rule-based framework adjusts trading behavior based on sentiment:

- **Extreme Fear**: Avoid trading or take minimal exposure.
- **Fear**: Selective trading with reduced position sizes.
- **Neutral**: Standard position sizing and trade frequency.
- **Greed**: Reduce position sizes and limit trade frequency.
- **Extreme Greed**: Minimize exposure and apply strict risk controls.

The goal is to control behavioral bias rather than predict market direction.
✅ BACKTEST (FIX INTERPRETATION)
## Backtest Results

| Metric             | Baseline      | Strategy      |
|--------------------|---------------|---------------|
| Total PnL         | 10,296,959    | 4,483,235     |
| Avg PnL per Trade | 48.75         | 22.05         |
| Win Rate          | 0.411         | 0.409         |
| Max Drawdown      | -443,038      | -221,519      |

The strategy significantly reduces maximum drawdown, at the cost of lower overall returns. This shows that sentiment-based rules improve downside protection, even though they reduce overall return potential.

Note: This is a simplified backtest and does not include transaction costs or slippage.
✅ KEY FINDINGS (SHARPENED)
## Key Findings

- Trading volume increases during Greed phases, but performance per trade declines.
- Extreme Greed shows higher win rates but significantly larger losses, indicating poor risk control.
- Fear conditions produce fewer but more selective trades with relatively stable outcomes.
- Neutral sentiment delivers the most consistent performance across metrics.
- Extreme Fear reduces participation, limiting both losses and opportunities.
- Loss magnitude is substantially higher in Greed compared to Neutral conditions.
- Position sizing is more effective in Fear conditions, while over-sizing in Greed reduces efficiency.
✅ STRATEGY RECOMMENDATIONS (FINAL SAFE)
## Strategy Recommendations

- Reduce position size and leverage during Greed and Extreme Greed conditions.
- Use sentiment as a risk-control filter rather than a directional trading signal.
- Limit trade frequency during high-activity Greed phases to reduce overtrading risk.
- Maintain consistent execution rules during Neutral conditions.
- Apply stricter stop-loss controls during sentiment extremes.
✅ INDUSTRY IMPACT (NO HYPE)
## Industry Impact

- Enables trading systems to adjust risk dynamically based on sentiment regimes.
- Helps reduce exposure to large losses during euphoric market conditions.
- Provides a framework for integrating behavioral signals into execution strategies.
- Supports more consistent performance by controlling sentiment-driven biases.
✅ SYSTEM ARCHITECTURE (KEEP SIMPLE)
## System Architecture

1. Data ingestion (trader data + sentiment index)
2. Data preprocessing and feature engineering
3. Sentiment-based merging
4. Rule-based decision engine
5. Output generation (adjusted trading behavior)

This pipeline can be extended into real-time systems.
✅ FUTURE WORK (STRONG SIGNAL)
## Future Work

- Real-time sentiment integration
- Machine learning models for loss prediction
- Intraday sentiment signals
- Integration with execution systems
✅ HOW TO RUN (KEEP CLEAN)
## How to Run

pip install -r requirements.txt  
python src/assignment_analysis.py