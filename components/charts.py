import plotly.express as px
import pandas as pd

def threat_distribution_chart():
    data = pd.DataFrame({
        "Category": ["Safe", "Phishing", "Suspicious"],
        "Count": [80, 15, 5]
    })

    fig = px.pie(
        data,
        names="Category",
        values="Count",
        title="Threat Distribution"
    )

    fig.update_layout(
        margin=dict(l=20, r=20, t=50, b=20),
        height=350
    )

    return fig