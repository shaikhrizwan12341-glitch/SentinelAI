import streamlit as st
import pandas as pd
from database.database import get_scans

st.set_page_config(
    page_title="Scan History",
    page_icon="📜",
    layout="wide"
)

st.title("📜 Scan History")

rows = get_scans()

if not rows:
    st.info("No scans available.")

else:

    df = pd.DataFrame(
        rows,
        columns=[
            "ID",
            "Scan Type",
            "Content",
            "Prediction",
            "Confidence",
            "Risk",
            "Scanned At"
        ]
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )