import datetime
import streamlit as st
import db_pinnacle as db

from config import SPORTS, PERIODS

# Add a bet
st.sidebar.write('Add a bet')

selected_sport = st.sidebar.selectbox(label='Select sport', options=SPORTS.keys(), index=None, placeholder='Start typing...')

if selected_sport is not None:

  selected_from_date = st.sidebar.date_input(label='Select start date', value = 'today', min_value=datetime.date(2021, 1, 1), help='Specify what date you want to start searching for fixtures.')

  if selected_from_date:

    selected_to_date = st.sidebar.date_input(label='Select end date', value = selected_from_date + datetime.timedelta(days=0), min_value=selected_from_date + datetime.timedelta(days=0), max_value=selected_from_date + datetime.timedelta(days=3), help='Specify what date you want to end your search. Please note that a maximum range of 3 days is allowed to avoid server overload.')
    
    if selected_to_date is not None:
  
      events = db.get_fixtures(sport_id=SPORTS[selected_sport], date_from=selected_from_date, date_to=selected_to_date)
  
      event_options = dict()
      for index, row in events.iterrows():
        if row['event_id'] not in event_options.keys():
          event_options.update({row['event_id']: f"{row['starts']} {row['league_name'].upper()} {row['runner_home']} - {row['runner_away']}"})
      
      selected_event = st.sidebar.selectbox(label='Select event', options=event_options.keys(), index=None, format_func=lambda x: event_options.get(x), placeholder='Start typing...')

      if selected_event is not None:

        odds = db.get_odds(event_id=selected_event)
        selected_market = st.sidebar.selectbox(label='Select market', options=odds.market.unique())

        if selected_market is not None:

          period_options = dict()
          for index, row in odds.iterrows():
            if row['market'] == selected_market and row['period'] not in period_options.keys():
              period_options.update({row['period']: PERIODS[(SPORTS[selected_sport], row['period'])]})

          selected_period = st.sidebar.selectbox(label='Select period', options=period_options.keys(), index=0, format_func=lambda x: period_options.get(x))          

        #st.sidebar.write(odds)
    
