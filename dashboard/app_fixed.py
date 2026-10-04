"""Fixed dashboard script (clean copy).

Use this as a drop-in replacement for dashboards/app.py if that file is corrupted.
Run CLI summary with: `python dashboards/app_fixed.py`
Or run interactive UI with: `streamlit run dashboards/app_fixed.py`
"""

from pathlib import Path
import sys

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
        print("Streamlit not installed — run CLI with `python dashboards/app_fixed.py`.")
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
