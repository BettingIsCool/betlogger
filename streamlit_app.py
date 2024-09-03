import streamlit as st
import db_pinnacle as db

# Add a bet
st.write('Add a bet')
unique_sports = db.get_sports()
st.write(unique_sports)
selected_sport = st.sidebar.selectbox(label='Sports', options=sorted(unique_sports))

