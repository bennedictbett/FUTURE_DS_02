import pandas as pd
import numpy as np
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')

RAW_DATA_PATH = Path("data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv")
PROCESSED_DATA_PATH = Path("data/processed/telco_cleaned.csv")


def load_data(path: Path = RAW_DATA_PATH) -> pd.DataFrame:
    logging.info(f"Loading data from: {path}")
    df = pd.read_csv(path)
    logging.info(f"Raw data shape: {df.shape}")
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Cleaning data...")
    df = df.copy()

    
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df["TotalCharges"] = df["TotalCharges"].fillna(df["MonthlyCharges"])

    
    df = df.drop_duplicates()

    
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    
    binary_cols = [
        "churn", "partner", "dependents", "phoneservice",
        "paperlessbilling", "multiplelines", "onlinesecurity",
        "onlinebackup", "deviceprotection", "techsupport",
        "streamingtv", "streamingmovies"
    ]
    for col in binary_cols:
        if col in df.columns:
            df[col] = df[col].map({
                "Yes": 1, "No": 0,
                "No phone service": 0,
                "No internet service": 0
            })

    df["seniorcitizen"] = df["seniorcitizen"].astype(int)

    
    df["tenure_band"] = pd.cut(
        df["tenure"],
        bins=[0, 12, 24, 36, 48, 60, 72],
        labels=["0–12 mo", "13–24 mo", "25–36 mo", "37–48 mo", "49–60 mo", "61–72 mo"],
        include_lowest=True
    )

    df["charge_band"] = pd.cut(
        df["monthlycharges"],
        bins=[0, 35, 65, 95, 120],
        labels=["Low", "Medium", "High", "Premium"]
    )

    service_cols = [
        "onlinesecurity", "onlinebackup", "deviceprotection",
        "techsupport", "streamingtv", "streamingmovies"
    ]
    df["num_services"]    = df[service_cols].sum(axis=1)
    df["lifetime_value"]  = df["tenure"] * df["monthlycharges"]
    df["churn_label"]     = df["churn"].map({1: "Churned", 0: "Retained"})

    logging.info(f"Cleaned data shape: {df.shape} | Churn rate: {df['churn'].mean():.2%}")
    return df


def save_clean_data(df: pd.DataFrame, path: Path = PROCESSED_DATA_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    logging.info(f"Saved to: {path}")


def run_pipeline() -> pd.DataFrame:
    df_raw   = load_data()
    df_clean = clean_data(df_raw)
    save_clean_data(df_clean)
    logging.info("Pipeline complete!")
    return df_clean


if __name__ == "__main__":
    df = run_pipeline()

