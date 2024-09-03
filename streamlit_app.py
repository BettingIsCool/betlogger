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

    event_options = dict()
    for index, row in events.iterrows():
      event_options.update({row['event_id']: f"{row['starts']} {row['league_name'].upper()} {row['runner_home']} - {row['runner_away']}"})
    
    selected_event = st.sidebar.selectbox(label='Select event', options=event_options.values(), index=None, format_func=lambda x: event_options.get(x), placeholder='Start typing...')
    
    #selected_event = st.sidebar.selectbox(label='Select league', options=sorted(leagues['league_name']), index=None, placeholder='Start typing...')
    
