import streamlit as st
import base64
from io import BytesIO
from PIL import Image


def display_image(image_path, width, margin_top=-35):
    """
    Display an image in a Streamlit app with the specified width and top margin.

    Args:
        image_path (str): The file path to the image to be displayed.
        width (int): The width of the image in pixels.
        margin_top (int, optional): The top margin for the image in pixels. Default is -35.
    """
    menu_logo = Image.open(image_path)
    
    # Convert image to base64 to display in markdown
    buffered = BytesIO()
    menu_logo.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    # Show image centered with reduced top margin
    st.markdown(
        f"""
        <div style='text-align: center; margin-top: {margin_top};'>
            <img src='data:image/png;base64,{img_str}' width='{width}'/>
        </div>
        """,
        unsafe_allow_html=True
    )