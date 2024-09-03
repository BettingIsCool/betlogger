import streamlit as st
import db_pinnacle as db

from config import SPORTS

# Add a bet
st.sidebar.write('Add a bet')
selected_sport = st.sidebar.selectbox(label='Select Sport', options=SPORTS.keys(), index=None, placeholder='Select Sport')

leagues = db.get_leagues(sport_id=SPORTS[selected_sport])
selected_league = st.sidebar.selectbox(label='Select League', options=leagues['league_name'])

