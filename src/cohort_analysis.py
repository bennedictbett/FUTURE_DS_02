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


# ── Cohort 1: Retention by Tenure Band & Contract ─────────────────────────────
def cohort_tenure_contract(df: pd.DataFrame) -> pd.DataFrame:
    cohort = df.groupby(
        ["tenure_band", "contract"], observed=True
    )["churn"].agg(total="count", churned="sum") \
     .assign(
         retention_rate=lambda x: 1 - (x["churned"] / x["total"]),
         churn_rate    =lambda x: x["churned"] / x["total"]
     ).reset_index()

    logging.info(f"\nCohort — Tenure x Contract:\n{cohort.to_string()}")
    return cohort


# ── Cohort 2: Retention heatmap (Tenure Band x Contract) ──────────────────────
def cohort_retention_heatmap(df: pd.DataFrame) -> pd.DataFrame:
    pivot = df.groupby(
        ["tenure_band", "contract"], observed=True
    )["churn"].mean().unstack("contract") * 100

    pivot = pivot.round(1)
    logging.info(f"\nRetention Heatmap Data:\n{pivot.to_string()}")

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(
        pivot,
        annot=True,
        fmt=".1f",
        cmap="RdYlGn_r",
        linewidths=0.5,
        linecolor="white",
        cbar_kws={"label": "Churn Rate (%)"},
        ax=ax
    )
    ax.set_title("Churn Rate Heatmap — Tenure Band vs Contract Type",
                 fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Contract Type")
    ax.set_ylabel("Tenure Band")
    plt.tight_layout()
    plt.savefig(FIGURES_PATH / "cohort_heatmap.png", dpi=150)
    plt.close()
    logging.info("Saved: cohort_heatmap.png")
    return pivot


# ── Cohort 3: Retention curve by contract type ────────────────────────────────
def retention_curve_by_contract(df: pd.DataFrame) -> None:
    cohort = df.groupby(
        ["tenure_band", "contract"], observed=True
    )["churn"].mean().reset_index()
    cohort["retention"] = (1 - cohort["churn"]) * 100

    fig, ax = plt.subplots(figsize=(10, 6))
    colors = {
        "Month-to-month": "#E24B4A",
        "One year"       : "#378ADD",
        "Two year"       : "#1D9E75"
    }
    for contract, group in cohort.groupby("contract"):
        ax.plot(
            group["tenure_band"].astype(str),
            group["retention"],
            marker="o",
            linewidth=2.5,
            markersize=7,
            label=contract,
            color=colors.get(contract, "#888")
        )

    ax.set_title("Retention Curve by Contract Type", fontsize=14, fontweight="bold")
    ax.set_xlabel("Tenure Band")
    ax.set_ylabel("Retention Rate (%)")
    ax.set_ylim(40, 105)
    ax.legend(title="Contract Type")
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig(FIGURES_PATH / "retention_curve_by_contract.png", dpi=150)
    plt.close()
    logging.info("Saved: retention_curve_by_contract.png")


# ── Cohort 4: Churn rate by tenure band & internet service ────────────────────
def cohort_tenure_internet(df: pd.DataFrame) -> None:
    cohort = df.groupby(
        ["tenure_band", "internetservice"], observed=True
    )["churn"].mean().reset_index()
    cohort["churn_rate"] = cohort["churn"] * 100

    fig, ax = plt.subplots(figsize=(10, 6))
    colors = {
        "Fiber optic": "#E24B4A",
        "DSL"        : "#378ADD",
        "No"         : "#1D9E75"
    }
    for service, group in cohort.groupby("internetservice"):
        ax.plot(
            group["tenure_band"].astype(str),
            group["churn_rate"],
            marker="o",
            linewidth=2.5,
            markersize=7,
            label=service,
            color=colors.get(service, "#888")
        )

    ax.set_title("Churn Rate by Tenure Band & Internet Service",
                 fontsize=14, fontweight="bold")
    ax.set_xlabel("Tenure Band")
    ax.set_ylabel("Churn Rate (%)")
    ax.set_ylim(0, 70)
    ax.legend(title="Internet Service")
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig(FIGURES_PATH / "cohort_tenure_internet.png", dpi=150)
    plt.close()
    logging.info("Saved: cohort_tenure_internet.png")


# ── Cohort 5: Customer count by tenure band (volume view) ─────────────────────
def cohort_volume_bar(df: pd.DataFrame) -> None:
    cohort = df.groupby(
        ["tenure_band", "churn_label"], observed=True
    ).size().unstack("churn_label").fillna(0)

    fig, ax = plt.subplots(figsize=(10, 6))
    cohort.plot(
        kind="bar",
        stacked=True,
        ax=ax,
        color=["#E24B4A", "#1D9E75"],
        edgecolor="white",
        linewidth=0.5
    )
    ax.set_title("Customer Volume by Tenure Band", fontsize=14, fontweight="bold")
    ax.set_xlabel("Tenure Band")
    ax.set_ylabel("Number of Customers")
    ax.legend(title="Status", labels=["Churned", "Retained"])
    ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(FIGURES_PATH / "cohort_volume.png", dpi=150)
    plt.close()
    logging.info("Saved: cohort_volume.png")


# ── Main ──────────────────────────────────────────────────────────────────────
def run_cohort_analysis(df: pd.DataFrame = None) -> None:
    if df is None:
        df = load_clean_data()

    logging.info("Running cohort analysis...")

    cohort_tenure_contract(df)
    cohort_retention_heatmap(df)
    retention_curve_by_contract(df)
    cohort_tenure_internet(df)
    cohort_volume_bar(df)

    logging.info("cohort_analysis.py complete!")


if __name__ == "__main__":
    run_cohort_analysis()
