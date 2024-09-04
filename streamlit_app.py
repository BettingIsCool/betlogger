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
      event_details = dict()
      for index, row in events.iterrows():
        if row['event_id'] not in event_options.keys():
          event_options.update({row['event_id']: f"{row['starts']} {row['league_name'].upper()} {row['runner_home']} - {row['runner_away']}"})
          event_details.update({row['event_id']: {'starts': row['starts'], 'league_id': row['league_id'], 'league_name': row['league_name'], 'runner_home': row['runner_home'], 'runner_away': row['runner_away']}})
      
      selected_event_id = st.sidebar.selectbox(label='Select event', options=event_options.keys(), index=None, format_func=lambda x: event_options.get(x), placeholder='Start typing...')

      if selected_event_id is not None:

        odds = db.get_odds(event_id=selected_event_id)
        selected_market = st.sidebar.selectbox(label='Select market', options=odds.market.unique(), index=0)

        if selected_market is not None:

          period_options = dict()
          for index, row in odds.iterrows():
            if row['market'] == selected_market and row['period'] not in period_options.keys():
              period_options.update({row['period']: PERIODS[(SPORTS[selected_sport], row['period'])]})

          selected_period = st.sidebar.selectbox(label='Select period', options=period_options.keys(), index=0, format_func=lambda x: period_options.get(x))

          if selected_period is not None:

            side_options = dict()
            for index, row in odds.iterrows():
              if selected_market == 'moneyline':
                if row['market'] == selected_market and row['period'] == selected_period:
                  if row['odds1'] is not None:
                    side_options.update({'odds1': event_details[selected_event_id]['runner_home']})
                  if row['odds0'] is not None:
                    side_options.update({'odds0': 'Draw'})
                  if row['odds2'] is not None:
                    side_options.update({'odds2': event_details[selected_event_id]['runner_away']})
              
              elif selected_market == 'spread':
                if row['market'] == selected_market and row['period'] == selected_period:
                  if row['odds1'] is not None:
                    side_options.update({'odds1': event_details[selected_event_id]['runner_home']})
                  if row['odds2'] is not None:
                    side_options.update({'odds2': event_details[selected_event_id]['runner_away']})
              
              elif selected_market in ('totals', 'home_totals', 'away_totals'):
                if row['market'] == selected_market and row['period'] == selected_period:
                  if row['odds1'] is not None:
                    side_options.update({'odds1': 'Over'})
                  if row['odds2'] is not None:
                    side_options.update({'odds2': 'Under'})

            selected_side = st.sidebar.selectbox(label='Select side', options=side_options.keys(), index=None, format_func=lambda x: side_options.get(x))

            selected_line = None
            if selected_side is not None and selected_market != 'moneyline':

              # Please note that the selected home line is returned even if the selection is 'away'
              line_options = dict()
              for index, row in odds.iterrows():
                if row['market'] == selected_market and row['period'] == selected_period and row[selected_side] is not None:
                  if row['market'] == 'spread' and selected_side == 'odds2':
                    line_options.update({row['line']: -row['line']})
                  else:
                    line_options.update({row['line']: row['line']})
              
              selected_line = st.sidebar.selectbox(label='Select line', options=line_options.keys(), index=None, format_func=lambda x: line_options.get(x))

            st.sidebar.write(selected_event_id, event_details[selected_event_id]['starts'], event_details[selected_event_id]['league_id'], event_details[selected_event_id]['league_name'], event_details[selected_event_id]['runner_home'], event_details[selected_event_id]['runner_away'], selected_market, selected_period, selected_side, selected_line)
  
