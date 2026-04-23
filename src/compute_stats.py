import pandas as pd

df = pd.read_csv("merged_dataset.csv")

# Group by sentiment_label
grouped = df.groupby("sentiment_label")

# Compute stats
stats = {}
for name, group in grouped:
    stats[name] = {
        "count": len(group),
        "avg_pnl": group["closedPnL"].mean(),
        "win_rate": (group["closedPnL"] > 0).mean(),
        "avg_leverage": group.get("leverage", pd.Series()).mean()
        if "leverage" in group.columns
        else None,
        "avg_loss": group[group["closedPnL"] < 0]["closedPnL"].mean(),
        "trade_count": len(group),
    }

print(stats)
