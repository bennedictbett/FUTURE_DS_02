import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')

PROCESSED_DATA_PATH = Path("data/processed/telco_segmented.csv")
FIGURES_PATH        = Path("reports/figures")
FIGURES_PATH.mkdir(parents=True, exist_ok=True)


def load_data(path: Path = PROCESSED_DATA_PATH) -> pd.DataFrame:
    return pd.read_csv(path)



def ltv_summary(df: pd.DataFrame) -> dict:
    avg_monthly   = df["monthlycharges"].mean()
    avg_tenure    = df["tenure"].mean()
    avg_ltv       = df["lifetime_value"].mean()
    median_ltv    = df["lifetime_value"].median()
    total_revenue = df["lifetime_value"].sum()

    # Churned vs retained 
    churned_ltv  = df[df["churn"] == 1]["lifetime_value"].mean()
    retained_ltv = df[df["churn"] == 0]["lifetime_value"].mean()

    # Revenue lost to churn
    revenue_lost = df[df["churn"] == 1]["lifetime_value"].sum()

    logging.info(f"Avg Monthly Charge : ${avg_monthly:,.2f}")
    logging.info(f"Avg Tenure         : {avg_tenure:.1f} months")
    logging.info(f"Avg LTV            : ${avg_ltv:,.2f}")
    logging.info(f"Median LTV         : ${median_ltv:,.2f}")
    logging.info(f"Total Revenue      : ${total_revenue:,.2f}")
    logging.info(f"Avg LTV Churned    : ${churned_ltv:,.2f}")
    logging.info(f"Avg LTV Retained   : ${retained_ltv:,.2f}")
    logging.info(f"Revenue Lost       : ${revenue_lost:,.2f}")

    return {
        "avg_monthly"   : avg_monthly,
        "avg_tenure"    : avg_tenure,
        "avg_ltv"       : avg_ltv,
        "median_ltv"    : median_ltv,
        "total_revenue" : total_revenue,
        "churned_ltv"   : churned_ltv,
        "retained_ltv"  : retained_ltv,
        "revenue_lost"  : revenue_lost
    }

def ltv_by_contract(df: pd.DataFrame) -> pd.DataFrame:
    result = df.groupby("contract")["lifetime_value"].agg(
        avg_ltv="mean",
        median_ltv="median",
        total_revenue="sum",
        customers="count"
    ).round(2)
    logging.info(f"\nLTV by Contract:\n{result.to_string()}")
    return result


def ltv_by_value_segment(df: pd.DataFrame) -> pd.DataFrame:
    result = df.groupby("value_segment", observed=True).agg(
        avg_ltv       =("lifetime_value", "mean"),
        avg_tenure    =("tenure", "mean"),
        avg_monthly   =("monthlycharges", "mean"),
        churn_rate    =("churn", "mean"),
        customers     =("churn", "count")
    ).round(2)
    logging.info(f"\nLTV by Value Segment:\n{result.to_string()}")
    return result


def revenue_loss_projection(df: pd.DataFrame) -> pd.DataFrame:
    projection = df.groupby("risk_segment", observed=True).agg(
        customers     =("churn", "count"),
        churn_rate    =("churn", "mean"),
        avg_monthly   =("monthlycharges", "mean")
    ).reset_index()

    projection["expected_churners"]   = (projection["customers"] * projection["churn_rate"]).round(0).astype(int)
    projection["monthly_rev_at_risk"] = (projection["expected_churners"] * projection["avg_monthly"]).round(2)
    projection["annual_rev_at_risk"]  = (projection["monthly_rev_at_risk"] * 12).round(2)

    logging.info(f"\nRevenue Loss Projection:\n{projection.to_string()}")
    return projection


def plot_ltv_by_contract(df: pd.DataFrame) -> None:
    data   = ltv_by_contract(df)
    colors = ["#E24B4A", "#378ADD", "#1D9E75"]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].bar(data.index, data["avg_ltv"], color=colors)
    axes[0].set_title("Avg Lifetime Value by Contract", fontweight="bold")
    axes[0].set_xlabel("Contract Type")
    axes[0].set_ylabel("Avg LTV ($)")
    for i, val in enumerate(data["avg_ltv"]):
        axes[0].text(i, val + 50, f"${val:,.0f}", ha="center", fontsize=10)

    axes[1].bar(data.index, data["total_revenue"], color=colors)
    axes[1].set_title("Total Revenue by Contract", fontweight="bold")
    axes[1].set_xlabel("Contract Type")
    axes[1].set_ylabel("Total Revenue ($)")
    for i, val in enumerate(data["total_revenue"]):
        axes[1].text(i, val + 1000, f"${val/1e6:.2f}M", ha="center", fontsize=10)

    fig.suptitle("Lifetime Value by Contract Type", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(FIGURES_PATH / "ltv_by_contract.png", dpi=150)
    plt.close()
    logging.info("Saved: ltv_by_contract.png")


def plot_ltv_distribution(df: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    churned  = df[df["churn"] == 1]["lifetime_value"]
    retained = df[df["churn"] == 0]["lifetime_value"]

    axes[0].hist(retained, bins=40, alpha=0.6, color="#1D9E75", label="Retained")
    axes[0].hist(churned,  bins=40, alpha=0.6, color="#E24B4A", label="Churned")
    axes[0].set_title("LTV Distribution: Churned vs Retained", fontweight="bold")
    axes[0].set_xlabel("Lifetime Value ($)")
    axes[0].set_ylabel("Number of Customers")
    axes[0].legend()

    data = df.groupby("tenure_band", observed=True)["lifetime_value"].mean()
    axes[1].plot(data.index.astype(str), data.values,
                 marker="o", color="#378ADD", linewidth=2.5, markersize=8)
    axes[1].fill_between(data.index.astype(str), data.values, alpha=0.15, color="#378ADD")
    axes[1].set_title("Avg LTV by Tenure Band", fontweight="bold")
    axes[1].set_xlabel("Tenure Band")
    axes[1].set_ylabel("Avg LTV ($)")

    fig.suptitle("Customer Lifetime Value Analysis", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(FIGURES_PATH / "ltv_distribution.png", dpi=150)
    plt.close()
    logging.info("Saved: ltv_distribution.png")


def plot_revenue_at_risk(df: pd.DataFrame) -> None:
    data   = revenue_loss_projection(df)
    colors = ["#1D9E75", "#378ADD", "#EF9F27", "#E24B4A"]

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(data["risk_segment"], data["annual_rev_at_risk"], color=colors)
    ax.set_title("Annual Revenue at Risk by Segment", fontsize=14, fontweight="bold")
    ax.set_xlabel("Risk Segment")
    ax.set_ylabel("Annual Revenue at Risk ($)")
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 500,
                f"${bar.get_height():,.0f}",
                ha="center", fontsize=10)
    plt.tight_layout()
    plt.savefig(FIGURES_PATH / "revenue_at_risk.png", dpi=150)
    plt.close()
    logging.info("Saved: revenue_at_risk.png")


def run_ltv_analysis(df: pd.DataFrame = None) -> dict:
    if df is None:
        df = load_data()

    logging.info("Running lifetime value analysis...")

    summary    = ltv_summary(df)
    ltv_by_contract(df)
    ltv_by_value_segment(df)
    revenue_loss_projection(df)

    plot_ltv_by_contract(df)
    plot_ltv_distribution(df)
    plot_revenue_at_risk(df)

    logging.info("lifetime_value.py complete!")
    return summary


if __name__ == "__main__":
    run_ltv_analysis()