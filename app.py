# app.py

import streamlit as st
from utils.auth_config import get_authenticator

# Load authenticator and config
authenticator, config = get_authenticator()

# Login
name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    authenticator.logout("Logout", "sidebar")
    st.sidebar.success(f"Welcome {name}")
    st.title("Retail Dashboard")
    st.write("📊 This is your dashboard.")
elif authentication_status is False:
    st.error("Incorrect username or password.")
elif authentication_status is None:
    st.warning("Please enter your credentials.")
