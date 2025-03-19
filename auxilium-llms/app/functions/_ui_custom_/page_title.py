import streamlit as st
from CONFIG import PATH_ICON_LOGO_AUXILIUM
from PIL import Image


def display_title(title):
    """
    Display the page title and favicon for a Streamlit app.

    Parameters:
    title (str): The title to set for the page.
    """
    favicon = Image.open(PATH_ICON_LOGO_AUXILIUM)
    st.set_page_config(
        page_title=title,
        page_icon=favicon,
    )

    st.markdown(
        f"""
        <style>
        .stAppDeployButton {{
            display: none;
        }}
        .stStatusWidget {{
            display: none;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )