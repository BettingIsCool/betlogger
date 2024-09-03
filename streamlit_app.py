import streamlit as st
import db_pinnacle as db

from config import SPORTS

# Add a bet
st.sidebar.write('Add a bet')

selected_sport = st.sidebar.selectbox(label='Sport', options=SPORTS.keys(), placeholder='Select sport')

leagues = db.get_leagues(sport_id=SPORTS[selected_sport])
selected_league = st.sidebar.selectbox(label='League', options=leagues['league_name'], index=585, placeholder='Select league')

