import streamlit as st
import db_pinnacle as db
import datetime

from config import SPORTS

# Add a bet
st.sidebar.write('Add a bet')

selected_sport = st.sidebar.selectbox(label='Select sport', options=SPORTS.keys(), index=None, placeholder='Start typing...')

if selected_sport is not None:

  selected_date = st.sidebar.date_input(label='Select event start time', value = 'today', min_value=datetime.date(2021, 1, 1))

  if selected_date is not None:

    events = db.get_fixtures(sport_id=SPORTS[selected_sport], starts=selected_date)

    st.sidebar.write(events)
    
    
    selected_event = st.sidebar.selectbox(label='Select league', options=sorted(leagues['league_name']), index=None, placeholder='Start typing...')
    
    if selected_league is not None:
      st.sidebar.write(leagues[leagues['league_name'] == selected_league]['league_id'])
