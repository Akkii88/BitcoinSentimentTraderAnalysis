import pandas as pd

# Define trading rules based on sentiment insights
TRADING_RULES = {
    "Extreme Fear": {
        "position_size_factor": 0.2,  # Small: Minimize exposure due to paralysis and poor timing
        "leverage_limit": 1.0,  # Low: Avoid amplifying losses
        "trade_frequency": "low",  # Rare trades to avoid missed opportunities
        "trade_allowed": False,  # Generally avoid trading in extreme fear
        "stop_loss_pct": 2.0,  # Tight: Quick exit on further downside
        "risk_limit_pct": 1.0,  # Conservative daily loss limit
    },
    "Fear": {
        "position_size_factor": 0.5,  # Medium: Selective, quality-focused
        "leverage_limit": 2.0,  # Moderate: Balance risk with rebound potential
        "trade_frequency": "medium",  # Balanced: Capture rebounds without overtrading
        "trade_allowed": True,
        "stop_loss_pct": 3.0,  # Moderate: Allow some room for recovery
        "risk_limit_pct": 2.0,
    },
    "Neutral": {
        "position_size_factor": 1.0,  # Large: Consistent, emotion-free performance
        "leverage_limit": 3.0,  # Standard: Optimize for Sharpe ratio
        "trade_frequency": "high",  # Frequent: Reliable conditions
        "trade_allowed": True,
        "stop_loss_pct": 5.0,  # Standard: Room for volatility
        "risk_limit_pct": 3.0,
    },
    "Greed": {
        "position_size_factor": 0.3,  # Small-Medium: Reduce due to overtrading and losses
        "leverage_limit": 1.5,  # Low: Control impulsivity-driven risks
        "trade_frequency": "medium",  # Controlled: Avoid erosion from high volume
        "trade_allowed": True,
        "stop_loss_pct": 4.0,  # Tighter: Cut losses on severe drops
        "risk_limit_pct": 2.5,
    },
    "Extreme Greed": {
        "position_size_factor": 0.1,  # Very Small: High asymmetry, severe downside
        "leverage_limit": 1.0,  # Minimal: Prevent catastrophic losses
        "trade_frequency": "low",  # Rare: Wait for pullbacks in euphoria
        "trade_allowed": False,  # Avoid unless contrarian
        "stop_loss_pct": 2.5,  # Very Tight: Immediate exit
        "risk_limit_pct": 1.5,
    },
}


def apply_trading_rules(df):
    """
    Apply rule-based trading system to the merged dataset.

    Args:
        df (pd.DataFrame): Merged dataset with 'sentiment_label' column.

    Returns:
        pd.DataFrame: DataFrame with added trading rule columns.
    """
    if "sentiment_label" not in df.columns:
        raise ValueError("DataFrame must contain 'sentiment_label' column")

    # Map rules to each row based on sentiment
    df = df.copy()
    df["position_size_factor"] = df["sentiment_label"].map(
        lambda x: TRADING_RULES.get(x, {}).get("position_size_factor", 0.5)
    )
    df["leverage_limit"] = df["sentiment_label"].map(
        lambda x: TRADING_RULES.get(x, {}).get("leverage_limit", 2.0)
    )
    df["trade_allowed"] = df["sentiment_label"].map(
        lambda x: TRADING_RULES.get(x, {}).get("trade_allowed", True)
    )
    df["stop_loss_pct"] = df["sentiment_label"].map(
        lambda x: TRADING_RULES.get(x, {}).get("stop_loss_pct", 5.0)
    )
    df["risk_limit_pct"] = df["sentiment_label"].map(
        lambda x: TRADING_RULES.get(x, {}).get("risk_limit_pct", 2.0)
    )

    # Optional: Flag high-risk trades based on PnL history (if available)
    if "closedPnL" in df.columns:
        df["high_risk_flag"] = (
            df["closedPnL"] < df["stop_loss_pct"] * -0.01
        )  # Example: If loss exceeds stop

    return df


# Example usage
if __name__ == "__main__":
    df = pd.read_csv("merged_dataset.csv")
    df_with_rules = apply_trading_rules(df)
    print(
        df_with_rules[
            [
                "sentiment_label",
                "position_size_factor",
                "leverage_limit",
                "trade_allowed",
            ]
        ].head()
    )
    # Save updated dataset
    df_with_rules.to_csv("merged_dataset_with_rules.csv", index=False)
