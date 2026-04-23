import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.style.use("ggplot")

# Load merged data
df = pd.read_csv("merged_dataset.csv")


# Analysis 1: Trade Frequency vs Performance
def trade_frequency_vs_performance(df):
    # Group by date and sentiment
    daily = (
        df.groupby(["trade_date", "sentiment_label"])
        .agg(
            trade_count=("Account", "count"),
            avg_pnl=("closedPnL", "mean"),
            total_pnl=("closedPnL", "sum"),
        )
        .reset_index()
    )

    # Scatter plot
    plt.figure(figsize=(10, 6))
    colors = {
        "Extreme Fear": "red",
        "Fear": "orange",
        "Neutral": "blue",
        "Greed": "green",
        "Extreme Greed": "purple",
    }
    for sentiment in df["sentiment_label"].dropna().unique():
        subset = daily[daily["sentiment_label"] == sentiment]
        plt.scatter(
            subset["trade_count"],
            subset["avg_pnl"],
            label=sentiment,
            alpha=0.7,
            color=colors.get(sentiment, "gray"),
            s=50,
        )
    plt.xlabel("Daily Trade Count", fontsize=12)
    plt.ylabel("Average PnL ($)", fontsize=12)
    plt.title(
        "Trade Frequency vs Performance by Sentiment", fontsize=14, fontweight="bold"
    )
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig("outputs/trade_freq_vs_perf.png", dpi=150, bbox_inches="tight")
    plt.close()

    # Correlation
    corr = daily[["trade_count", "avg_pnl"]].corr()
    print(f"Correlation between trade count and avg PnL: {corr.iloc[0, 1]:.2f}")


# Analysis 2: Extreme Loss Analysis
def extreme_loss_analysis(df):
    # Top 10% losses
    losses = df[df["closedPnL"] < 0]["closedPnL"]
    threshold = losses.quantile(0.1)  # Top 10% worst losses
    extreme_losses = df[df["closedPnL"] <= threshold]

    # By sentiment
    extreme_by_sentiment = extreme_losses.groupby("sentiment_label").agg(
        count=("closedPnL", "count"),
        avg_extreme_loss=("closedPnL", "mean"),
        total_extreme_loss=("closedPnL", "sum"),
    )
    print("Extreme Losses by Sentiment:")
    print(extreme_by_sentiment)

    # Histogram of extreme losses
    extreme_losses["closedPnL"].hist(bins=50)
    plt.title("Distribution of Extreme Losses")
    plt.xlabel("PnL")
    plt.ylabel("Frequency")
    plt.savefig("outputs/extreme_losses_dist.png")
    plt.close()


# Analysis 3: Symbol-Level Sentiment Sensitivity
def symbol_sentiment_sensitivity(df):
    if "Coin" in df.columns:
        symbol_sentiment = (
            df.groupby(["Coin", "sentiment_label"])
            .agg(
                trade_count=("Account", "count"),
                avg_pnl=("closedPnL", "mean"),
                win_rate=("is_profit", "mean"),
            )
            .reset_index()
        )

        # Pivot for heatmap
        pivot_pnl = symbol_sentiment.pivot(
            index="Coin", columns="sentiment_label", values="avg_pnl"
        )
        pivot_pnl.plot(kind="bar", figsize=(12, 8), colormap="viridis")
        plt.title("Average PnL by Symbol and Sentiment", fontsize=14, fontweight="bold")
        plt.ylabel("Avg PnL ($)", fontsize=12)
        plt.xlabel("Symbol", fontsize=12)
        plt.xticks(rotation=45, ha="right")
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.tight_layout()
        plt.savefig("outputs/symbol_sentiment_pnl.png", dpi=150, bbox_inches="tight")
        plt.close()

        print("Top symbols by sentiment sensitivity:")
        for sentiment in pivot_pnl.columns:
            top_symbol = pivot_pnl[sentiment].idxmax()
            print(
                f"{sentiment}: {top_symbol} (PnL: {pivot_pnl.loc[top_symbol, sentiment]:.2f})"
            )


# Analysis 4: Volatility of Returns
def volatility_of_returns(df):
    sentiment_vol = df.groupby("sentiment_label")["closedPnL"].std()
    print("PnL Volatility by Sentiment:")
    print(sentiment_vol)

    # Boxplot for visualization
    df.boxplot(
        column="closedPnL",
        by="sentiment_label",
        figsize=(10, 6),
        patch_artist=True,
        boxprops=dict(facecolor="lightcoral"),
        medianprops=dict(color="black"),
    )
    plt.title("PnL Volatility by Market Sentiment", fontsize=14, fontweight="bold")
    plt.suptitle("")
    plt.ylabel("PnL ($)", fontsize=12)
    plt.xlabel("Sentiment Level", fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig("outputs/pnl_volatility_boxplot.png", dpi=150, bbox_inches="tight")
    plt.close()


# Analysis 5: PnL vs Trade Size Interaction
def pnl_vs_trade_size(df):
    if "trade_notional" in df.columns:
        # Scatter with color by sentiment
        sentiments = df["sentiment_label"].dropna().unique()
        for sent in sentiments:
            subset = df[df["sentiment_label"] == sent]
            plt.scatter(
                subset["trade_notional"],
                subset["closedPnL"],
                label=sent,
                alpha=0.5,
                s=10,
            )
        plt.xlabel("Trade Notional")
        plt.ylabel("Closed PnL")
        plt.title("PnL vs Trade Size by Sentiment")
        plt.legend()
        plt.yscale("symlog")  # Handle large ranges
        plt.savefig("outputs/pnl_vs_size.png")
        plt.close()

        # Correlation by sentiment
        for sent in sentiments:
            subset = df[df["sentiment_label"] == sent]
            if len(subset) > 10:
                corr = subset[["trade_notional", "closedPnL"]].corr().iloc[0, 1]
                print(f"Correlation PnL vs Size in {sent}: {corr:.2f}")


# Analysis 5: Extreme Loss Behavior
def extreme_loss_behavior(df):
    losses = df[df["closedPnL"] < 0]["closedPnL"]
    threshold = losses.quantile(0.1)
    extreme_losses = df[df["closedPnL"] <= threshold]

    sentiments = sorted(extreme_losses["sentiment_label"].dropna().unique())
    fig, axes = plt.subplots(1, len(sentiments), figsize=(15, 5), sharey=True)
    colors = {
        "Extreme Fear": "red",
        "Fear": "orange",
        "Neutral": "blue",
        "Greed": "green",
        "Extreme Greed": "purple",
    }

    for i, sent in enumerate(sentiments):
        subset = extreme_losses[extreme_losses["sentiment_label"] == sent]
        axes[i].hist(
            subset["closedPnL"], bins=20, alpha=0.7, color=colors.get(sent, "gray")
        )
        axes[i].set_title(f"Extreme Losses: {sent}")
        axes[i].set_xlabel("PnL ($)")
    axes[0].set_ylabel("Frequency")
    plt.tight_layout()
    plt.savefig("outputs/extreme_loss_behavior.png", dpi=150, bbox_inches="tight")
    plt.close()

    stats = extreme_losses.groupby("sentiment_label")["closedPnL"].agg(
        ["count", "mean", "min"]
    )
    print("Extreme Loss Stats by Sentiment:")
    print(stats)


# Analysis 6: Risk vs Reward Patterns
def risk_reward_patterns(df):
    risk_reward = df.groupby("sentiment_label").agg(
        win_rate=("is_profit", "mean"),
        avg_loss=("closedPnL", lambda x: x[x < 0].mean() if (x < 0).any() else 0),
        avg_win=("closedPnL", lambda x: x[x > 0].mean() if (x > 0).any() else 0),
    )

    plt.figure(figsize=(8, 6))
    plt.scatter(
        risk_reward["win_rate"], -risk_reward["avg_loss"], s=100, c="blue", alpha=0.7
    )
    for sent in risk_reward.index:
        plt.text(
            risk_reward.loc[sent, "win_rate"],
            -risk_reward.loc[sent, "avg_loss"],
            sent,
            fontsize=10,
            ha="right",
        )
    plt.xlabel("Win Rate")
    plt.ylabel("Avg Loss Magnitude ($)")
    plt.title("Risk vs Reward: Win Rate vs Loss Severity by Sentiment")
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig("outputs/risk_reward_patterns.png", dpi=150, bbox_inches="tight")
    plt.close()

    print("Risk-Reward Metrics:")
    print(risk_reward)


# Run analyses
trade_frequency_vs_performance(df)
symbol_sentiment_sensitivity(df)
volatility_of_returns(df)
extreme_loss_behavior(df)
risk_reward_patterns(df)
