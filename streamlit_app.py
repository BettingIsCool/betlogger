import streamlit as st
import db_pinnacle as db

# Switch to wide-mode for better view
st.set_page_config(layout="wide")

# Add a bet
st.write('Add a bet')
unique_sports = db.get_sports()
st.write(unique_sports)
selected_sport = st.selectbox(label='Sports', options=sorted(unique_sports))

