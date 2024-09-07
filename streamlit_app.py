import datetime
import pandas as pd
import streamlit as st
import db_pinnacle as db
import streamlit_authenticator as stauth

from config import SPORTS, PERIODS, BOOKS

# Fetch all active users from database
users = db.get_users()

# Create credential lists for authentication
names = [item['name'] for item in users]
usernames = [item['username'] for item in users]
passwords = [item['password'] for item in users]

# Create hashed passwords for secure login
hashed_passwords = stauth.Hasher(passwords).generate()
authenticator = stauth.Authenticate(names, usernames, hashed_passwords, 'app_home', 'auth', cookie_expiry_days=0)
name, authentication_status, username = authenticator.login("Login", "sidebar")

# Display text if authentication fails
if authentication_status is False:
  st.error("Username/password incorrect or subscription expired.")

# Continue if authentication suceeds
if authentication_status:

  # Display name & widgets in side bar
  st.sidebar.title(f"Welcome {name}")
  
  # Add a bet
  st.sidebar.write('Add a bet')
  
  selected_sport = st.sidebar.selectbox(label='Select sport', options=SPORTS.keys(), index=None, placeholder='Start typing...', help='41 unique sports supported.')
  
  if selected_sport is not None:
  
    selected_from_date = st.sidebar.date_input(label='Select start date', value = 'today', min_value=datetime.date(2021, 1, 1), help='Specify what date you want to start searching for fixtures. You can either use the calendar or manually enter the date, i.e. 2024/08/19.')
  
    if selected_from_date:
  
      selected_to_date = st.sidebar.date_input(label='Select end date', value = selected_from_date + datetime.timedelta(days=0), min_value=selected_from_date + datetime.timedelta(days=0), max_value=selected_from_date + datetime.timedelta(days=3), help='Specify what date you want to end your search. Please note that a maximum range of 3 days is allowed to avoid excess server load.')
      
      if selected_to_date is not None:
    
        events = db.get_fixtures(sport_id=SPORTS[selected_sport], date_from=selected_from_date, date_to=selected_to_date)
    
        event_options = dict()
        event_details = dict()
        for index, row in events.iterrows():
          if row['event_id'] not in event_options.keys():
            event_options.update({row['event_id']: f"{row['starts']} {row['league_name'].upper()} {row['runner_home']} - {row['runner_away']}"})
            event_details.update({row['event_id']: {'starts': row['starts'], 'league_id': row['league_id'], 'league_name': row['league_name'], 'runner_home': row['runner_home'], 'runner_away': row['runner_away']}})
        
        selected_event_id = st.sidebar.selectbox(label='Select event', options=event_options.keys(), index=None, format_func=lambda x: event_options.get(x), placeholder='Start typing...', help='Start searching your fixture by typing any league, home team, away team. Only fixtures with available closing odds are listed.')
  
        if selected_event_id is not None:
  
          odds = db.get_odds(event_id=selected_event_id)
          selected_market = st.sidebar.selectbox(label='Select market', options=odds.market.unique(), index=0, help='Only markets with available closing odds are listed.')
  
          if selected_market is not None:
  
            period_options = dict()
            for index, row in odds.iterrows():
              if row['market'] == selected_market and row['period'] not in period_options.keys():
                period_options.update({row['period']: PERIODS[(SPORTS[selected_sport], row['period'])]})
  
            selected_period = st.sidebar.selectbox(label='Select period', options=period_options.keys(), index=0, format_func=lambda x: period_options.get(x), help='Only periods with available closing odds are listed.')
  
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
                
                selected_line = st.sidebar.selectbox(label='Select line', options=line_options.keys(), index=None, format_func=lambda x: line_options.get(x), help='Only lines with available closing odds are listed.')

              odds = st.sidebar.number_input("Enter odds", min_value=1.001, value=2.000, step=0.01, format="%0.3f")
              stake = st.sidebar.number_input("Enter stake", min_value=0.01, value=1.00, step=1.00, format="%0.2f")
              book = st.sidebar.selectbox("Select bookmaker", options=sorted(BOOKS))
              tag = st.sidebar.text_input("Enter tag", max_chars=25, help='You can add a custom string to classify this bet as something that you may want to research in a future analysis. This could be a particular strategy that you are following, a tipster, etc.')
  
              data = dict()
              data.update({'user': username})
              data.update({'tag': tag})
              data.update({'starts': event_details[selected_event_id]['starts']})
              data.update({'sport_id': SPORTS[selected_sport]})
              data.update({'sport_name': selected_sport})
              data.update({'league_id': event_details[selected_event_id]['league_id']})
              data.update({'league_name': event_details[selected_event_id]['league_name']})
              data.update({'event_id': selected_event_id})  
              data.update({'runner_home': event_details[selected_event_id]['runner_home']})
              data.update({'runner_away': event_details[selected_event_id]['runner_away']})
              data.update({'market': selected_market})
              data.update({'period': selected_period})
              data.update({'side': selected_side})
              data.update({'raw_line': selected_line}) if selected_line is not None else data.update({'raw_line': None})
              data.update({'odds': odds})
              data.update({'stake': stake})
              data.update({'bookmaker': book})

              bet_added = st.sidebar.button('Add bet')

              if bet_added:

                db.append_bet(data=data)

  # Apply filter to recorded bets
  st.sidebar.write('Apply filters to your bets')
  
  user_unique_sports = db.get_user_unique_sports(username=username)
  selected_sports = st.sidebar.multiselect(label='Sports', options=sorted(user_unique_sports), default=user_unique_sports)
  selected_sports = [f"'{s}'" for s in selected_sports]
  selected_sports = f"({','.join(selected_sports)})"

  if selected_sports != '()':
    
    user_unique_leagues = db.get_user_unique_leagues(username=username, sports=selected_sports)
    selected_leagues = st.sidebar.multiselect(label='Leagues', options=sorted(user_unique_leagues), default=user_unique_leagues)
    selected_leagues = [f"'{s}'" for s in selected_leagues]
    selected_leagues = f"({','.join(selected_leagues)})"

    if selected_leagues != '()':
  
      user_unique_bookmakers = db.get_user_unique_bookmakers(username=username, sports=selected_sports, leagues=selected_leagues)
      selected_bookmakers = st.sidebar.multiselect(label='Bookmakers', options=sorted(user_unique_bookmakers), default=user_unique_bookmakers)
      selected_bookmakers = [f"'{s}'" for s in selected_bookmakers]
      selected_bookmakers = f"({','.join(selected_bookmakers)})"

      if selected_bookmakers != '()':
        
        user_unique_tags = db.get_user_unique_tags(username=username, sports=selected_sports, leagues=selected_leagues, bookmakers=selected_bookmakers)
        selected_tags = st.sidebar.multiselect(label='Tags', options=sorted(user_unique_tags), default=user_unique_tags)
        selected_tags = [f"'{s}'" for s in selected_tags]
        selected_tags = f"({','.join(selected_tags)})"
        
        if selected_tags != '()':

          bets = db.get_bets(username=username, sports=selected_sports, leagues=selected_leagues, bookmakers=selected_bookmakers, tags=selected_tags)
          
          bets_df = pd.DataFrame(bets)
          st.legacy_dataframe(data=bets_df, width=1000, use_container_width=True, hide_index=True)                
                
    
