import pandas as pd
import matplotlib.pyplot as plt
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')

PROCESSED_DATA_PATH = Path("data/processed/telco_cleaned.csv")
FIGURES_PATH        = Path("reports/figures")
FIGURES_PATH.mkdir(parents=True, exist_ok=True)


def load_clean_data(path: Path = PROCESSED_DATA_PATH) -> pd.DataFrame:
    return pd.read_csv(path)


def overall_churn_rate(df: pd.DataFrame) -> dict:
    total      = len(df)
    churned    = df["churn"].sum()
    retained   = total - churned
    churn_rate = churned / total

    logging.info(f"Total     : {total:,}")
    logging.info(f"Churned   : {churned:,} ({churn_rate:.2%})")
    logging.info(f"Retained  : {retained:,} ({1 - churn_rate:.2%})")

    return {"total": total, "churned": churned,
            "retained": retained, "churn_rate": churn_rate}


def churn_by(df: pd.DataFrame, col: str) -> pd.DataFrame:
    return (
        df.groupby(col, observed=True)["churn"]
        .agg(total="count", churned="sum")
        .assign(churn_rate=lambda x: x["churned"] / x["total"])
        .sort_values("churn_rate", ascending=False)
    )


def plot_bar(data: pd.DataFrame, title: str, filename: str,
             color: str = "#E24B4A", horizontal: bool = False) -> None:
    fig, ax = plt.subplots(figsize=(9, 5))
    values = data["churn_rate"] * 100
    labels = data.index.astype(str)

    if horizontal:
        bars = ax.barh(labels, values, color=color)
        ax.set_xlabel("Churn Rate (%)")
        ax.set_xlim(0, values.max() + 10)
        for bar in bars:
            ax.text(bar.get_width() + 0.5,
                    bar.get_y() + bar.get_height() / 2,
                    f"{bar.get_width():.1f}%", va="center", fontsize=10)
    else:
        bars = ax.bar(labels, values, color=color)
        ax.set_ylabel("Churn Rate (%)")
        ax.set_ylim(0, values.max() + 10)
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 0.8,
                    f"{bar.get_height():.1f}%", ha="center", fontsize=10)

    ax.set_title(title, fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(FIGURES_PATH / filename, dpi=150)
    plt.close()
    logging.info(f"Saved: {filename}")


def plot_tenure_line(df: pd.DataFrame) -> None:
    data = churn_by(df, "tenure_band").sort_index()
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(data.index.astype(str), data["churn_rate"] * 100,
            marker="o", color="#E24B4A", linewidth=2.5, markersize=8)
    ax.fill_between(data.index.astype(str),
                    data["churn_rate"] * 100, alpha=0.15, color="#E24B4A")
    ax.set_title("Churn Rate by Tenure Band", fontsize=14, fontweight="bold")
    ax.set_xlabel("Tenure Band")
    ax.set_ylabel("Churn Rate (%)")
    ax.set_ylim(0, 60)
    plt.tight_layout()
    plt.savefig(FIGURES_PATH / "churn_by_tenure.png", dpi=150)
    plt.close()
    logging.info("Saved: churn_by_tenure.png")


def run_metrics(df: pd.DataFrame = None) -> dict:
    if df is None:
        df = load_clean_data()

    logging.info("Running churn metrics...")
    metrics = overall_churn_rate(df)

    
    for col, label in [
        ("contract",      "Contract"),
        ("internetservice","Internet Service"),
        ("paymentmethod", "Payment Method"),
        ("charge_band",   "Charge Band"),
        ("tenure_band",   "Tenure Band"),
    ]:
        result = churn_by(df, col)
        logging.info(f"\nChurn by {label}:\n{result.to_string()}")


    plot_bar(churn_by(df, "contract"),
             "Churn Rate by Contract Type",
             "churn_by_contract.png",
             color="#E24B4A")

    plot_bar(churn_by(df, "paymentmethod"),
             "Churn Rate by Payment Method",
             "churn_by_payment.png",
             color="#378ADD", horizontal=True)

    plot_bar(churn_by(df, "internetservice"),
             "Churn Rate by Internet Service",
             "churn_by_internet.png",
             color="#1D9E75")

    plot_tenure_line(df)

    logging.info("churn_metrics.py complete!")
    return metrics


if __name__ == "__main__":
    run_metrics()