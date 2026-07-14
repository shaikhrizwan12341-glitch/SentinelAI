import streamlit as st

def metric_card(title, value, icon, color="#1f77b4"):
    st.markdown(
        f"""
        <div style="
            background-color:#1e293b;
            padding:20px;
            border-radius:15px;
            border-left:6px solid {color};
            box-shadow:0 3px 8px rgba(0,0,0,0.3);
            margin-bottom:15px;
        ">
            <h4 style="margin:0;color:white;">
                {icon} {title}
            </h4>

            <h1 style="
                margin-top:15px;
                color:white;
            ">
                {value}
            </h1>
        </div>
        """,
        unsafe_allow_html=True
    )