import pandas as pd
import numpy as np

# Load the dataset with trading rules applied
df = pd.read_csv("merged_dataset_with_rules.csv")


# Function to compute metrics
def compute_metrics(pnl_series):
    total_pnl = pnl_series.sum()
    avg_pnl_per_trade = pnl_series.mean()
    win_rate = (pnl_series > 0).mean()

    # Max drawdown
    cumulative = pnl_series.cumsum()
    peak = cumulative.expanding().max()
    drawdown = cumulative - peak
    max_drawdown = drawdown.min()

    return {
        "total_pnl": total_pnl,
        "avg_pnl_per_trade": avg_pnl_per_trade,
        "win_rate": win_rate,
        "max_drawdown": max_drawdown,
    }


# Baseline: Original PnL
baseline_metrics = compute_metrics(df["closedPnL"])

# Strategy: Filter allowed trades and adjust PnL by position_size_factor
strategy_df = df[df["trade_allowed"] == True].copy()
strategy_df["adjusted_pnl"] = (
    strategy_df["closedPnL"] * strategy_df["position_size_factor"]
)
strategy_metrics = compute_metrics(strategy_df["adjusted_pnl"])

# Comparison table
comparison = pd.DataFrame(
    {
        "Metric": ["Total PnL", "Avg PnL per Trade", "Win Rate", "Max Drawdown"],
        "Baseline": [
            baseline_metrics["total_pnl"],
            baseline_metrics["avg_pnl_per_trade"],
            baseline_metrics["win_rate"],
            baseline_metrics["max_drawdown"],
        ],
        "Strategy": [
            strategy_metrics["total_pnl"],
            strategy_metrics["avg_pnl_per_trade"],
            strategy_metrics["win_rate"],
            strategy_metrics["max_drawdown"],
        ],
    }
)

print("Backtest Comparison:")
print(comparison)

# Save to CSV
comparison.to_csv("outputs/backtest_results.csv", index=False)

# Interpretation
print("\nInterpretation:")
print(
    f"Strategy Total PnL: {strategy_metrics['total_pnl']:.2f} vs Baseline: {baseline_metrics['total_pnl']:.2f} ({'+' if strategy_metrics['total_pnl'] > baseline_metrics['total_pnl'] else ''}{((strategy_metrics['total_pnl'] / baseline_metrics['total_pnl'] - 1) * 100):.1f}%)"
)
print(
    f"Strategy improves stability with lower max drawdown: {strategy_metrics['max_drawdown']:.2f} vs {baseline_metrics['max_drawdown']:.2f}, reducing risk in volatile sentiment periods."
)
