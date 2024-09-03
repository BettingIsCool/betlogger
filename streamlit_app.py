import streamlit as st
import db_pinnacle as db

# Switch to wide-mode for better view
st.set_page_config(layout="wide")

# Add a bet
unique_sports = db.get_sports()
selected_sports = st.selectbox(label='Sports', options=sorted(unique_sports))
