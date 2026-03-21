import pandas as pd
import numpy as np
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')

SEGMENTED_DATA_PATH = Path("data/processed/telco_segmented.csv")
EXPORT_PATH         = Path("data/processed/telco_powerbi.xlsx")


def load_data(path: Path = SEGMENTED_DATA_PATH) -> pd.DataFrame:
    return pd.read_csv(path)


# ── Table 1: Main customer table ──────────────────────────────────────────────
def build_customer_table(df: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "customerid", "gender", "seniorcitizen", "partner",
        "dependents", "tenure", "tenure_band", "contract",
        "internetservice", "paymentmethod", "paperlessbilling",
        "monthlycharges", "totalcharges", "lifetime_value",
        "num_services", "charge_band", "churn", "churn_label",
        "risk_segment", "value_segment", "behavior_segment"
    ]
    table = df[cols].copy()
    logging.info(f"Customer table: {table.shape}")
    return table


# ── Table 2: Churn metrics summary ────────────────────────────────────────────
def build_churn_summary(df: pd.DataFrame) -> pd.DataFrame:
    total    = len(df)
    churned  = df["churn"].sum()
    retained = total - churned

    summary = pd.DataFrame([{
        "total_customers"   : total,
        "churned"           : churned,
        "retained"          : retained,
        "churn_rate"        : round(churned / total, 4),
        "retention_rate"    : round(retained / total, 4),
        "avg_monthly_charge": round(df["monthlycharges"].mean(), 2),
        "avg_tenure_months" : round(df["tenure"].mean(), 1),
        "avg_ltv"           : round(df["lifetime_value"].mean(), 2),
        "total_revenue"     : round(df["lifetime_value"].sum(), 2),
        "revenue_lost"      : round(df[df["churn"] == 1]["lifetime_value"].sum(), 2),
    }])
    logging.info(f"Churn summary table: {summary.shape}")
    return summary


# ── Table 3: Churn by contract ────────────────────────────────────────────────
def build_churn_by_contract(df: pd.DataFrame) -> pd.DataFrame:
    table = df.groupby("contract")["churn"].agg(
        total="count", churned="sum"
    ).assign(
        churn_rate    =lambda x: (x["churned"] / x["total"]).round(4),
        retention_rate=lambda x: 1 - (x["churned"] / x["total"]).round(4)
    ).reset_index()
    logging.info(f"Churn by contract table: {table.shape}")
    return table


# ── Table 4: Churn by tenure band ─────────────────────────────────────────────
def build_churn_by_tenure(df: pd.DataFrame) -> pd.DataFrame:
    table = df.groupby("tenure_band", observed=True)["churn"].agg(
        total="count", churned="sum"
    ).assign(
        churn_rate    =lambda x: (x["churned"] / x["total"]).round(4),
        retention_rate=lambda x: 1 - (x["churned"] / x["total"]).round(4)
    ).reset_index()
    logging.info(f"Churn by tenure table: {table.shape}")
    return table


# ── Table 5: Cohort heatmap table ─────────────────────────────────────────────
def build_cohort_table(df: pd.DataFrame) -> pd.DataFrame:
    table = df.groupby(
        ["tenure_band", "contract"], observed=True
    )["churn"].agg(
        total="count", churned="sum"
    ).assign(
        churn_rate    =lambda x: (x["churned"] / x["total"]).round(4),
        retention_rate=lambda x: 1 - (x["churned"] / x["total"]).round(4)
    ).reset_index()
    logging.info(f"Cohort table: {table.shape}")
    return table


# ── Table 6: Risk segment summary ─────────────────────────────────────────────
def build_risk_summary(df: pd.DataFrame) -> pd.DataFrame:
    table = df.groupby("risk_segment", observed=True).agg(
        customers          =("churn", "count"),
        churned            =("churn", "sum"),
        churn_rate         =("churn", "mean"),
        avg_monthly        =("monthlycharges", "mean"),
        avg_ltv            =("lifetime_value", "mean"),
        total_revenue      =("lifetime_value", "sum")
    ).round(2).reset_index()
    table["annual_rev_at_risk"] = (
        table["customers"] * table["churn_rate"] * table["avg_monthly"] * 12
    ).round(2)
    logging.info(f"Risk summary table: {table.shape}")
    return table


# ── Table 7: LTV by contract ──────────────────────────────────────────────────
def build_ltv_by_contract(df: pd.DataFrame) -> pd.DataFrame:
    table = df.groupby("contract").agg(
        customers     =("lifetime_value", "count"),
        avg_ltv       =("lifetime_value", "mean"),
        median_ltv    =("lifetime_value", "median"),
        total_revenue =("lifetime_value", "sum"),
        avg_tenure    =("tenure", "mean"),
        avg_monthly   =("monthlycharges", "mean")
    ).round(2).reset_index()
    logging.info(f"LTV by contract table: {table.shape}")
    return table


# ── Table 8: Churn by payment method ─────────────────────────────────────────
def build_churn_by_payment(df: pd.DataFrame) -> pd.DataFrame:
    table = df.groupby("paymentmethod")["churn"].agg(
        total="count", churned="sum"
    ).assign(
        churn_rate=lambda x: (x["churned"] / x["total"]).round(4)
    ).reset_index()
    logging.info(f"Churn by payment table: {table.shape}")
    return table


# ── Table 9: Churn by internet service ───────────────────────────────────────
def build_churn_by_internet(df: pd.DataFrame) -> pd.DataFrame:
    table = df.groupby("internetservice")["churn"].agg(
        total="count", churned="sum"
    ).assign(
        churn_rate=lambda x: (x["churned"] / x["total"]).round(4)
    ).reset_index()
    logging.info(f"Churn by internet table: {table.shape}")
    return table


# ── Export to Excel ───────────────────────────────────────────────────────────
def export_to_excel(tables: dict, path: Path = EXPORT_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with pd.ExcelWriter(path, engine="xlsxwriter") as writer:
        workbook = writer.book

        # Formats
        header_fmt = workbook.add_format({
            "bold": True, "bg_color": "#378ADD",
            "font_color": "white", "border": 1,
            "align": "center", "valign": "vcenter"
        })
        pct_fmt  = workbook.add_format({"num_format": "0.00%"})
        usd_fmt  = workbook.add_format({"num_format": "$#,##0.00"})
        num_fmt  = workbook.add_format({"num_format": "#,##0"})

        for sheet_name, df_table in tables.items():
            df_table.to_excel(writer, sheet_name=sheet_name, index=False)
            worksheet = writer.sheets[sheet_name]

            # Style header row
            for col_num, col_name in enumerate(df_table.columns):
                worksheet.write(0, col_num, col_name, header_fmt)

            # Auto-fit columns
            for col_num, col_name in enumerate(df_table.columns):
                max_len = max(
                    df_table[col_name].astype(str).map(len).max(),
                    len(col_name)
                ) + 4
                # Apply number formats
                if "rate" in col_name:
                    worksheet.set_column(col_num, col_num, max_len, pct_fmt)
                elif any(x in col_name for x in ["revenue", "ltv", "monthly", "charges"]):
                    worksheet.set_column(col_num, col_num, max_len, usd_fmt)
                elif any(x in col_name for x in ["total", "customers", "churned", "retained"]):
                    worksheet.set_column(col_num, col_num, max_len, num_fmt)
                else:
                    worksheet.set_column(col_num, col_num, max_len)

            logging.info(f"Written sheet: {sheet_name}")

    logging.info(f"Excel file saved to: {path}")


# ── Main ──────────────────────────────────────────────────────────────────────
def run_export(df: pd.DataFrame = None) -> None:
    if df is None:
        df = load_data()

    logging.info("Building Power BI export tables...")

    tables = {
        "Customers"          : build_customer_table(df),
        "Churn Summary"      : build_churn_summary(df),
        "Churn by Contract"  : build_churn_by_contract(df),
        "Churn by Tenure"    : build_churn_by_tenure(df),
        "Cohort Table"       : build_cohort_table(df),
        "Risk Segments"      : build_risk_summary(df),
        "LTV by Contract"    : build_ltv_by_contract(df),
        "Churn by Payment"   : build_churn_by_payment(df),
        "Churn by Internet"  : build_churn_by_internet(df),
    }

    export_to_excel(tables, EXPORT_PATH)
    logging.info("export_for_powerbi.py complete!")


if __name__ == "__main__":
    run_export()
