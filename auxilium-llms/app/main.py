import streamlit as st
import os
from CONFIG import RAG_API, MAX_UPLOAD_SIZE_MB
from app_pages.menu import menu_page
from app_pages.discussion import discussion_page
from app_pages.documents import documents_page
from functions._ui_custom_.page_title import display_title


# ----[Max Upload Size Data File Streamlit Config]----
config_path = os.path.expanduser("~/.streamlit/config.toml")
os.makedirs(os.path.dirname(config_path), exist_ok=True)
with open(config_path, "w") as config_file:
    config_file.write(f"[server]\nmaxUploadSize = {MAX_UPLOAD_SIZE_MB}\n")


# ----[Interface Title & Navigation]----
display_title("Auxilium")

pages = [
    st.Page(menu_page, title="Menu", icon="🌐"),
    st.Page(discussion_page, title="Discussion", icon="💬"),
]

if RAG_API:
    pages.append(st.Page(documents_page, title="Documents", icon="📚"))

navigation = st.navigation(pages, position="sidebar")
navigation.run()