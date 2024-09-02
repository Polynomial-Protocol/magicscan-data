import streamlit as st
from st_pages import Page, show_pages

from magicscan_data import Data

PAGE_PREFIX = "dashboard/" if st.secrets.settings.IS_CLOUD == "true" else ""

st.set_page_config(
    page_title="MagicScan Dashboards",
    page_icon=f"{PAGE_PREFIX}static/favicon.ico",
    layout="wide",
)

hide_footer = """
    <style>
        footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_footer, unsafe_allow_html=True)

Data.main()
