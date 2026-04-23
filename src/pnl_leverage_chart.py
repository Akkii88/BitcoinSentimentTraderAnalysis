import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("merged_dataset.csv")

# Use 'Size Tokens' as leverage proxy (since actual leverage not available)
# Bucket into Low, Medium, High
df["leverage_bucket"] = pd.qcut(df["size"], q=3, labels=["Low", "Medium", "High"])

# Group by sentiment and leverage bucket, compute avg PnL
grouped = (
    df.groupby(["sentiment_label", "leverage_bucket"])["closedpnl"].mean().reset_index()
)

# Plot: Bar chart grouped by sentiment
sentiments = sorted(df["sentiment_label"].dropna().unique())
fig, ax = plt.subplots(figsize=(10, 6))

bar_width = 0.15
x_positions = range(len(grouped["leverage_bucket"].unique()))

for i, sent in enumerate(sentiments):
    subset = grouped[grouped["sentiment_label"] == sent]
    ax.bar(
        [x + i * bar_width for x in x_positions],
        subset["closedpnl"],
        width=bar_width,
        label=sent,
        alpha=0.7,
    )

ax.set_xlabel("Leverage Bucket (Size)", fontsize=12)
ax.set_ylabel("Average PnL ($)", fontsize=12)
ax.set_title("PnL vs Leverage by Sentiment", fontsize=14, fontweight="bold")
ax.set_xticks([x + bar_width for x in x_positions])
ax.set_xticklabels(["Low", "Medium", "High"])
ax.legend()
ax.grid(axis="y", linestyle="--", alpha=0.7)

plt.tight_layout()
plt.savefig("outputs/pnl_vs_leverage_sentiment.png", dpi=150, bbox_inches="tight")
plt.close()

print("Chart saved: outputs/pnl_vs_leverage_sentiment.png")
