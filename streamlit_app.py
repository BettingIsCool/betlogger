import datetime
import streamlit as st
import db_pinnacle as db
from streamlit_date_picker import date_range_picker, PickerType, Unit, date_picker

from config import SPORTS

# Add a bet
st.sidebar.write('Add a bet')

selected_sport = st.sidebar.selectbox(label='Select sport', options=SPORTS.keys(), index=None, placeholder='Start typing...')

if selected_sport is not None:

  #selected_date = st.sidebar.date_input(label='Select event start time', value = 'today', min_value=datetime.date(2021, 1, 1))
  date_range_string = date_range_picker(picker_type=PickerType.time.string_value,
                                      start=-1, end=0, unit=Unit.days.string_value,
                                      key='range_picker',
                                      refresh_button={'is_show': True, 'button_name': 'Refresh last 1Days',
                                                      'refresh_date': -1,
                                                      'unit': Unit.days.string_value})
  if datetime_string is not None:
      st.write(date_range_string)
  
      if selected_date is not None:
    
        events = db.get_fixtures(sport_id=SPORTS[selected_sport], starts=selected_date)
    
        event_options = dict()
        for index, row in events.iterrows():
          event_options.update({row['event_id']: f"{row['starts']} {row['league_name'].upper()} {row['runner_home']} - {row['runner_away']}"})
        
        selected_event = st.sidebar.selectbox(label='Select event', options=event_options.keys(), index=None, format_func=lambda x: event_options.get(x), placeholder='Start typing...')
        
        st.sidebar.write(selected_event)
    
