"""Retail Sales Forecasting dashboard.

Loads prediction CSVs from `output/` and provides a Streamlit UI (if available)
or a CLI summary fallback. The script guards missing dependencies and prints
clear instructions when required packages are not installed.
"""

from pathlib import Path

# Guard imports so the script fails gracefully when dependencies are missing
try:
    import pandas as pd
except Exception:
    pd = None

try:
    import numpy as np
except Exception:
    np = None

try:
    import streamlit as st
except Exception:
    st = None

try:
    import plotly.express as px
    import plotly.graph_objects as go
except Exception:
    px = None
    go = None


def safe_r2(y_true, y_pred):
    if np is None:
        return None
    try:
        y_true = np.array(y_true, dtype=float)
        y_pred = np.array(y_pred, dtype=float)
        mask = ~np.isnan(y_true) & ~np.isnan(y_pred)
        if mask.sum() == 0:
            return None
        yt = y_true[mask]
        yp = y_pred[mask]
        ss_res = np.sum((yt - yp) ** 2)
        ss_tot = np.sum((yt - yt.mean()) ** 2)
        if ss_tot == 0:
            return None
        return 1.0 - ss_res / ss_tot
    except Exception:
        return None


def load_csv_if_exists(path: Path):
    if pd is None:
        return None
    if path.exists():
        try:
            return pd.read_csv(path)
        except Exception:
            return None
    return None


def load_predictions():
    if pd is None:
        return None, None
    candidates = [
        Path("../output/sales_predictions_enriched.csv"),
        Path("../output/sales_predictions.csv"),
        Path("output/sales_predictions_enriched.csv"),
        Path("output/sales_predictions.csv"),
    ]
    for p in candidates:
        if p.exists():
            try:
                return pd.read_csv(p), p
            except Exception:
                continue
    return None, None


def run_streamlit():
    if st is None:
        print("Streamlit not installed — run CLI with `python dashboards/app.py`.")
        return
    if pd is None or np is None:
        st.error("Install pandas and numpy to use this dashboard.")
        return

    st.set_page_config(page_title="Retail Sales Forecasting", layout="wide")
    st.title("Retail Sales Forecasting Dashboard")

    preds, src = load_predictions()
    st.sidebar.write("Predictions:", str(src) if src else "missing")

    if preds is None:
        st.warning("No predictions found.")
        return

    df = preds.copy()
    if "Predicted" in df.columns:
        df["Predicted"] = pd.to_numeric(df["Predicted"], errors="coerce")
    if "Actual" in df.columns:
        df["Actual"] = pd.to_numeric(df["Actual"], errors="coerce")

    st.write(f"Loaded: {src} — {len(df)} rows")

    if "Actual" in df.columns:
        mae = np.nanmean(np.abs(df["Actual"] - df["Predicted"]))
        rmse = np.sqrt(np.nanmean((df["Actual"] - df["Predicted"]) ** 2))
        r2 = safe_r2(df["Actual"], df["Predicted"])
        c1, c2, c3 = st.columns(3)
        c1.metric("MAE", f"{mae:,.2f}")
        c2.metric("RMSE", f"{rmse:,.2f}")
        c3.metric("R²", f"{r2:.3f}" if r2 is not None else "N/A")

        if px is not None:
            fig = px.scatter(df, x="Actual", y="Predicted", title="Actual vs Predicted")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No Actual values in predictions file.")
        st.dataframe(df.head(200))


def cli_summary():
    if pd is None or np is None:
        print("Install pandas and numpy: pip install -r requirements.txt")
        return
    preds, src = load_predictions()
    if preds is None:
        print("No predictions found in output/.")
        return
    df = preds.copy()
    print(f"Loaded: {src} — {len(df)} rows")
    if "Actual" in df.columns:
        df["Predicted"] = pd.to_numeric(df["Predicted"], errors="coerce")
        df["Actual"] = pd.to_numeric(df["Actual"], errors="coerce")
        mae = np.nanmean(np.abs(df["Actual"] - df["Predicted"]))
        rmse = np.sqrt(np.nanmean((df["Actual"] - df["Predicted"]) ** 2))
        r2 = safe_r2(df["Actual"], df["Predicted"])
        print(f"MAE: {mae:.2f}, RMSE: {rmse:.2f}, R2: {r2:.3f}" if r2 is not None else f"MAE: {mae:.2f}, RMSE: {rmse:.2f}")
    print(df.head(10).to_string(index=False))


if __name__ == "__main__":
    if st is None:
        cli_summary()
    else:
        run_streamlit()

        sales_df = pd.read_csv(
    "data/processed/clean_retail_sales.csv"
)

sales_df["date"] = pd.to_datetime(sales_df["date"])


sales_df["year"] = sales_df["date"].dt.year
sales_df["month"] = sales_df["date"].dt.month

st.sidebar.header("Dashboard Filters")

store_list = sorted(sales_df["store_id"].unique())

selected_stores = st.sidebar.multiselect(
    "Select Stores",
    store_list,
    default=store_list[:5]
)

filtered_df = sales_df[
    sales_df["store_id"].isin(selected_stores)
]


####business KPI cards
st.subheader("Retail Performance Overview")

total_sales = filtered_df["weekly_sales"].sum()
avg_sales = filtered_df["weekly_sales"].mean()
store_count = filtered_df["store_id"].nunique()

c1, c2, c3 = st.columns(3)

c1.metric(
    "Total Sales",
    f"{total_sales:,.0f}"
)

c2.metric(
    "Average Weekly Sales",
    f"{avg_sales:,.0f}"
)

c3.metric(
    "Selected Stores",
    store_count
)


####Weekly Sales Trend #####
#This chart shows how total sales changed over time.

weekly_trend = (
    filtered_df
    .groupby("date")["weekly_sales"]
    .sum()
    .reset_index()
)

fig_weekly = px.line(
    weekly_trend,
    x="date",
    y="weekly_sales",
    title="Weekly Sales Trend"
)

st.plotly_chart(
    fig_weekly,
    use_container_width=True
)

store_sales = (
    filtered_df
    .groupby("store_id")["weekly_sales"]
    .sum()
    .reset_index()
    .sort_values(
        "weekly_sales",
        ascending=False
    )
)

fig_store = px.bar(
    store_sales,
    x="store_id",
    y="weekly_sales",
    title="Store-wise Sales Performance"
)

st.plotly_chart(
    fig_store,
    use_container_width=True
)

monthly_sales = (
    filtered_df
    .groupby(["year", "month"])["weekly_sales"]
    .sum()
    .reset_index()
)

monthly_sales["year_month"] = (
    monthly_sales["year"].astype(str)
    + "-"
    + monthly_sales["month"].astype(str).str.zfill(2)
)

fig_month = px.line(
    monthly_sales,
    x="year_month",
    y="weekly_sales",
    title="Monthly Sales Trend"
)

st.plotly_chart(
    fig_month,
    use_container_width=True
)

holiday_sales = (
    filtered_df
    .groupby("is_holiday_sales")["weekly_sales"]
    .mean()
    .reset_index()
)

# -----------------------------
# HOLIDAY IMPACT
# -----------------------------

holiday_col = None

if "is_holiday" in filtered_df.columns:
    holiday_col = "is_holiday"

elif "is_holiday_sales" in filtered_df.columns:
    holiday_col = "is_holiday_sales"

elif "is_holiday_features" in filtered_df.columns:
    holiday_col = "is_holiday_features"

elif "holiday" in filtered_df.columns:
    holiday_col = "holiday"


if holiday_col is not None:

    holiday_sales = (
        filtered_df
        .groupby(holiday_col)["weekly_sales"]
        .mean()
        .reset_index()
    )

    holiday_sales["holiday_status"] = (
        holiday_sales[holiday_col]
        .astype(str)
        .replace({
            "True": "Holiday",
            "False": "Non-Holiday",
            "1": "Holiday",
            "0": "Non-Holiday"
        })
    )

    fig_holiday = px.bar(
        holiday_sales,
        x="holiday_status",
        y="weekly_sales",
        title="Holiday vs Non-Holiday Average Sales",
        labels={
            "holiday_status": "Holiday Status",
            "weekly_sales": "Average Weekly Sales"
        }
    )

    st.plotly_chart(
        fig_holiday,
        use_container_width=True
    )

else:
    st.warning(
        "Holiday column was not found in the dataset."
    )



fig_holiday = px.bar(
    holiday_sales,
    x="holiday_status",
    y="weekly_sales",
    title="Holiday vs Non-Holiday Average Sales",
    labels={
        "holiday_status": "Holiday Status",
        "weekly_sales": "Average Weekly Sales"
    }
)



if "dept_id" in filtered_df.columns:

    dept_sales = (
        filtered_df
        .groupby("dept_id")["weekly_sales"]
        .sum()
        .reset_index()
        .sort_values(
            "weekly_sales",
            ascending=False
        )
        .head(10)
    )

    fig_dept = px.bar(
        dept_sales,
        x="dept_id",
        y="weekly_sales",
        title="Top 10 Departments by Sales"
    )

    st.plotly_chart(
        fig_dept,
        use_container_width=True
    )


st.markdown("---")

st.header("Machine Learning Forecasting")

st.markdown("---")

st.subheader("Retail Dataset Preview")

st.dataframe(
    filtered_df.head(100),
    use_container_width=True
)

# -----------------------------
# HOLIDAY IMPACT
# -----------------------------

holiday_col = None

if "is_holiday" in filtered_df.columns:
    holiday_col = "is_holiday"

elif "is_holiday_sales" in filtered_df.columns:
    holiday_col = "is_holiday_sales"

elif "is_holiday_features" in filtered_df.columns:
    holiday_col = "is_holiday_features"


if holiday_col is not None:

    holiday_sales = (
        filtered_df
        .groupby(holiday_col)["weekly_sales"]
        .mean()
        .reset_index()
    )

    holiday_sales["holiday_status"] = holiday_sales[
        holiday_col
    ].replace({
        True: "Holiday",
        False: "Non-Holiday",
        1: "Holiday",
        0: "Non-Holiday"
    })

    fig_holiday = px.bar(
        holiday_sales,
        x="holiday_status",
        y="weekly_sales",
        title="Holiday vs Non-Holiday Average Sales"
    )

    st.plotly_chart(
        fig_holiday,
        use_container_width=True
    )

else:
    st.warning("Holiday column was not found in the dataset.")













