import streamlit as st
import db_pinnacle as db

from config import SPORTS

# Add a bet
st.sidebar.write('Add a bet')
selected_sport = st.sidebar.selectbox(label='Sports', options=SPORTS.keys())

leagues = db.get_leagues(sport_id=SPORTS[selected_sport])
st.sidebar.write(leagues['league_name'])

