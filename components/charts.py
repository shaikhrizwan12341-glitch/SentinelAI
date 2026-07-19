import plotly.express as px
import pandas as pd

from database.database import (
    get_safe_scans,
    get_phishing_scans
)


def threat_distribution_chart():

    data = pd.DataFrame({
        "Category": [
            "Safe",
            "Phishing"
        ],
        "Count": [
            get_safe_scans(),
            get_phishing_scans()
        ]
    })

    fig = px.pie(
        data,
        names="Category",
        values="Count",
        title="Threat Distribution",
        hole=0.45
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    return fig