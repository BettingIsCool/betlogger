import streamlit as st
import db_pinnacle as db

from config import SPORTS

# Add a bet
st.sidebar.write('Add a bet')
selected_sport, selected_league = None, None

while selected_sport is None and selected_league is None:
  selected_sport = st.sidebar.selectbox(options=SPORTS.keys(), index=None, placeholder='Select Sport')
  
  leagues = db.get_leagues(sport_id=SPORTS[selected_sport])
  selected_league = st.sidebar.selectbox(label='Select League', options=leagues['league_name'])

