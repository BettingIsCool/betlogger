import streamlit as st
import db_pinnacle as db

from config import SPORTS

# Add a bet
st.sidebar.write('Add a bet')

selected_sport = st.sidebar.selectbox(label='Select sport', options=SPORTS.keys(), index=None, placeholder='Start typing...')

if selected_sport is not None:

  leagues = db.get_leagues(sport_id=SPORTS[selected_sport])
  selected_league = st.sidebar.selectbox(label='Select league', options=leagues['league_name'], index=None, placeholder='Start typing...')
  
  if selected_league is not None:
    st.sidebar.write(leagues[leagues['league_name'] == selected_league]['league_id'])

