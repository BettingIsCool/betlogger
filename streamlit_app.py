import datetime
import streamlit as st
import db_pinnacle as db
from streamlit_date_picker import date_range_picker, PickerType, Unit, date_picker

from config import SPORTS

# Add a bet
st.sidebar.write('Add a bet')

selected_sport = st.sidebar.selectbox(label='Select sport', options=SPORTS.keys(), index=None, placeholder='Start typing...')

if selected_sport is not None:

  selected_from_date = st.sidebar.date_input(label='Select date from', value = 'today', min_value=datetime.date(2021, 1, 1), help='Specify what date you want to start searching for fixtures.')

  if selected_from_date:

    selected_to_date = st.sidebar.date_input(label='Select date to', value = selected_from_date + datetime.timedelta(days=3), max_value=selected_from_date + datetime.timedelta(days=10), help='Specify what date you want to end your search. Please note that a maximum range of 10 days is allowed.')
    
    if selected_to_date is not None:
  
      events = db.get_fixtures(sport_id=SPORTS[selected_sport], starts=selected_date)
  
      event_options = dict()
      for index, row in events.iterrows():
        event_options.update({row['event_id']: f"{row['starts']} {row['league_name'].upper()} {row['runner_home']} - {row['runner_away']}"})
      
      selected_event = st.sidebar.selectbox(label='Select event', options=event_options.keys(), index=None, format_func=lambda x: event_options.get(x), placeholder='Start typing...')
      
      st.sidebar.write(selected_event)
    
