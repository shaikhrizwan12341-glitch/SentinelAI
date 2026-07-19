import streamlit as st

def metric_card(title, value, icon, color="#1f77b4"):

    value = str(value)

    html = f"""
    <div style="
        background-color:#1e293b;
        padding:20px;
        border-radius:15px;
        border-left:6px solid {color};
        box-shadow:0 3px 8px rgba(0,0,0,0.3);
        margin-bottom:15px;
    ">

        <div style="
            color:white;
            font-size:28px;
            font-weight:bold;
            margin-bottom:20px;
        ">
            {icon} {title}
        </div>

        <div style="
            color:white;
            font-size:42px;
            font-weight:bold;
        ">
            {value}
        </div>

    </div>
    """

    st.markdown(html, unsafe_allow_html=True)