import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')

PROCESSED_DATA_PATH = Path("data/processed/telco_cleaned.csv")
FIGURES_PATH        = Path("reports/figures")
FIGURES_PATH.mkdir(parents=True, exist_ok=True)


def load_clean_data(path: Path = PROCESSED_DATA_PATH) -> pd.DataFrame:
    return pd.read_csv(path)


def assign_risk_segment(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["risk_score"] = (
        (df["contract"] == "Month-to-month").astype(int) * 3 +
        (df["tenure"] <= 12).astype(int)                * 2 +
        (df["internetservice"] == "Fiber optic").astype(int) * 2 +
        (df["paymentmethod"] == "Electronic check").astype(int) * 1 +
        (df["monthlycharges"] > 65).astype(int)         * 1
    )

    df["risk_segment"] = pd.cut(
        df["risk_score"],
        bins=[-1, 2, 4, 6, 9],
        labels=["Low Risk", "Medium Risk", "High Risk", "Critical Risk"]
    )

    logging.info(f"\nRisk Segment Distribution:\n{df['risk_segment'].value_counts().to_string()}")
    logging.info(f"\nChurn Rate by Risk Segment:\n"
                 f"{df.groupby('risk_segment', observed=True)['churn'].mean().mul(100).round(2).to_string()}")
    return df


def assign_value_segment(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    percentiles = df["lifetime_value"].quantile([0.25, 0.50, 0.75])
    df["value_segment"] = pd.cut(
        df["lifetime_value"],
        bins=[-1,
              percentiles[0.25],
              percentiles[0.50],
              percentiles[0.75],
              df["lifetime_value"].max() + 1],
        labels=["Low Value", "Mid Value", "High Value", "Top Value"]
    )

    logging.info(f"\nValue Segment Distribution:\n{df['value_segment'].value_counts().to_string()}")
    logging.info(f"\nChurn Rate by Value Segment:\n"
                 f"{df.groupby('value_segment', observed=True)['churn'].mean().mul(100).round(2).to_string()}")
    return df


def assign_behavior_segment(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    conditions = [
        (df["tenure"] <= 12) & (df["contract"] == "Month-to-month"),
        (df["tenure"] > 12)  & (df["contract"] == "Month-to-month"),
        (df["contract"] == "One year"),
        (df["contract"] == "Two year")
    ]
    labels = ["New & Flexible", "Established & Flexible",
              "Committed (1yr)", "Loyal (2yr)"]

    df["behavior_segment"] = np.select(conditions, labels, default="Other")

    logging.info(f"\nBehavior Segment Distribution:\n"
                 f"{pd.Series(df['behavior_segment']).value_counts().to_string()}")
    logging.info(f"\nChurn Rate by Behavior Segment:\n"
                 f"{df.groupby('behavior_segment')['churn'].mean().mul(100).round(2).to_string()}")
    return df


def plot_risk_segments(df: pd.DataFrame) -> None:
    data = df.groupby("risk_segment", observed=True).agg(
        customers=("churn", "count"),
        churn_rate=("churn", "mean")
    ).reset_index()

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    
    colors = ["#1D9E75", "#378ADD", "#EF9F27", "#E24B4A"]
    axes[0].bar(data["risk_segment"], data["customers"], color=colors)
    axes[0].set_title("Customers by Risk Segment", fontweight="bold")
    axes[0].set_xlabel("Risk Segment")
    axes[0].set_ylabel("Number of Customers")
    for i, (val, label) in enumerate(zip(data["customers"], data["risk_segment"])):
        axes[0].text(i, val + 30, f"{val:,}", ha="center", fontsize=10)


    axes[1].bar(data["risk_segment"], data["churn_rate"] * 100, color=colors)
    axes[1].set_title("Churn Rate by Risk Segment", fontweight="bold")
    axes[1].set_xlabel("Risk Segment")
    axes[1].set_ylabel("Churn Rate (%)")
    axes[1].set_ylim(0, 80)
    for i, val in enumerate(data["churn_rate"] * 100):
        axes[1].text(i, val + 1, f"{val:.1f}%", ha="center", fontsize=10)

    fig.suptitle("Customer Risk Segmentation", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(FIGURES_PATH / "risk_segments.png", dpi=150)
    plt.close()
    logging.info("Saved: risk_segments.png")


def plot_value_segments(df: pd.DataFrame) -> None:
    data = df.groupby("value_segment", observed=True).agg(
        customers  =("churn", "count"),
        churn_rate =("churn", "mean"),
        avg_ltv    =("lifetime_value", "mean"),
        avg_tenure =("tenure", "mean")
    ).reset_index()

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    colors = ["#378ADD", "#1D9E75", "#EF9F27", "#E24B4A"]

    axes[0].bar(data["value_segment"], data["avg_ltv"], color=colors)
    axes[0].set_title("Avg Lifetime Value by Segment", fontweight="bold")
    axes[0].set_xlabel("Value Segment")
    axes[0].set_ylabel("Avg Lifetime Value ($)")
    for i, val in enumerate(data["avg_ltv"]):
        axes[0].text(i, val + 50, f"${val:,.0f}", ha="center", fontsize=10)

    axes[1].bar(data["value_segment"], data["churn_rate"] * 100, color=colors)
    axes[1].set_title("Churn Rate by Value Segment", fontweight="bold")
    axes[1].set_xlabel("Value Segment")
    axes[1].set_ylabel("Churn Rate (%)")
    axes[1].set_ylim(0, 60)
    for i, val in enumerate(data["churn_rate"] * 100):
        axes[1].text(i, val + 1, f"{val:.1f}%", ha="center", fontsize=10)

    fig.suptitle("Customer Value Segmentation", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(FIGURES_PATH / "value_segments.png", dpi=150)
    plt.close()
    logging.info("Saved: value_segments.png")


def plot_behavior_segments(df: pd.DataFrame) -> None:
    data = df.groupby("behavior_segment")["churn"].agg(
        total="count",
        churned="sum"
    ).assign(churn_rate=lambda x: x["churned"] / x["total"]) \
     .sort_values("churn_rate", ascending=True)

    fig, ax = plt.subplots(figsize=(10, 5))
    colors = ["#1D9E75", "#378ADD", "#EF9F27", "#E24B4A"]
    bars = ax.barh(data.index, data["churn_rate"] * 100, color=colors)
    ax.set_title("Churn Rate by Behavior Segment", fontsize=14, fontweight="bold")
    ax.set_xlabel("Churn Rate (%)")
    ax.set_xlim(0, 65)
    for bar in bars:
        ax.text(bar.get_width() + 0.5,
                bar.get_y() + bar.get_height() / 2,
                f"{bar.get_width():.1f}%", va="center", fontsize=10)
    plt.tight_layout()
    plt.savefig(FIGURES_PATH / "behavior_segments.png", dpi=150)
    plt.close()
    logging.info("Saved: behavior_segments.png")


def run_segmentation(df: pd.DataFrame = None) -> pd.DataFrame:
    if df is None:
        df = load_clean_data()

    logging.info("Running segmentation...")

    df = assign_risk_segment(df)
    df = assign_value_segment(df)
    df = assign_behavior_segment(df)

    plot_risk_segments(df)
    plot_value_segments(df)
    plot_behavior_segments(df)

    output_path = Path("data/processed/telco_segmented.csv")
    df.to_csv(output_path, index=False)
    logging.info(f"Saved segmented data to: {output_path}")

    logging.info("segmentation.py complete!")
    return df


if __name__ == "__main__":
    run_segmentation()
