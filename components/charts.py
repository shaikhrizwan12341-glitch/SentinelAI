import plotly.express as px
import pandas as pd

from database.database import (
    get_threat_distribution,
    get_scan_type_distribution,
    get_daily_scans
)


def threat_distribution_chart():
    rows = get_threat_distribution()

    if not rows:
        return px.pie(
            names=["No Data"],
            values=[1],
            title="Threat Distribution"
        )

    df = pd.DataFrame(rows, columns=["Prediction", "Count"])

    fig = px.pie(
        df,
        names="Prediction",
        values="Count",
        title="Threat Distribution"
    )

    fig.update_layout(height=350)

    return fig


def scan_type_chart():
    rows = get_scan_type_distribution()

    if not rows:
        return px.bar(
            x=["No Data"],
            y=[0],
            title="Scan Type Distribution"
        )

    df = pd.DataFrame(rows, columns=["Scan Type", "Count"])

    fig = px.bar(
        df,
        x="Scan Type",
        y="Count",
        title="Scan Type Distribution"
    )

    fig.update_layout(height=350)

    return fig


def daily_scan_chart():
    rows = get_daily_scans()

    if not rows:
        return px.line(
            x=[],
            y=[],
            title="Daily Scan Trend"
        )

    df = pd.DataFrame(rows, columns=["Date", "Scans"])

    fig = px.line(
        df,
        x="Date",
        y="Scans",
        markers=True,
        title="Daily Scan Trend"
    )

    fig.update_layout(height=350)

    return fig