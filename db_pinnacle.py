import streamlit as st
from sqlalchemy import text
from datetime import datetime
from config import TABLE_LEAGUES, TABLE_FIXTURES, TABLE_ODDS, TABLE_RESULTS, TABLE_BETS, TABLE_USERS

conn = st.connection('pinnacle', type='sql')


@st.cache_data(ttl=10)
def get_leagues(sport_id: int):

  return conn.query(f"SELECT league_id, league_name FROM {TABLE_LEAGUES} WHERE sport_id = {sport_id}", ttl=600)


@st.cache_data(ttl=10)
def get_fixtures(sport_id: int, date_from: datetime, date_to: datetime):

  return conn.query(f"SELECT DISTINCT(f.event_id), f.league_id, f.league_name, f.starts, f.runner_home, f.runner_away FROM {TABLE_FIXTURES} f, {TABLE_ODDS} o, {TABLE_RESULTS} r WHERE f.sport_id = {sport_id} AND DATE(f.starts) >= '{date_from.strftime('%Y-%m-%d')}' AND DATE(f.starts) <= '{date_to.strftime('%Y-%m-%d')}' AND o.event_id = f.event_id AND r.event_id = f.event_id ORDER BY f.starts", ttl=600)


@st.cache_data(ttl=10)
def get_odds(event_id: int):

  return conn.query(f"SELECT period, market, line, odds1, odds0, odds2 FROM {TABLE_ODDS} WHERE event_id = {event_id}", ttl=600)


@st.cache_data(ttl=10)
def get_users():

  return conn.query(f"SELECT name, username, password FROM {TABLE_USERS}", ttl=600).to_dict('records')


def append_bet(data: dict):

  query = f"INSERT INTO {TABLE_BETS} (user, tag, starts, sport_id, sport_name, league_id, league_name, event_id, runner_home, runner_away, market, period, side, raw_line, odds, stake) VALUES(:user, :tag, :starts, :sport_id, :sport_name, :league_id, :league_name, :event_id, :runner_home, :runner_away, :market, :period, :side, :raw_line, :odds, :stake)"
 
  with conn.session as session:
    session.execute(text(query), params = dict(user = data['user'], tag = data['tag'], starts = data['starts'], sport_id = data['sport_id'], sport_name = data['sport_name'], league_id = data['league_id'], league_name = data['league_name'], event_id = data['event_id'], runner_home = data['runner_home'], runner_away = data['runner_away'], market = data['market'], period = data['period'], side = data['side'], raw_line = data['raw_line'], odds = data['odds'], stake = data['stake']))
    session.commit()


@st.cache_data(ttl=10)
def get_bets(username: str, sport_ids: str):

  return conn.query(f"SELECT tag, starts, sport_name, league_name, runner_home, runner_away, market, period_name, side_name, line, odds, stake, bookmaker, bet_status, score_home, score_away, profit, ev, clv, bet_added FROM {TABLE_BETS} WHERE user = '{username}' AND sport_id IN {sport_ids} ORDER BY starts", ttl=600).to_dict('records')


@st.cache_data(ttl=10)
def get_user_unique_sports(username: str):

  return conn.query(f"SELECT DISTINCT(sport_name) FROM {TABLE_BETS} WHERE user = '{username}'", ttl=600)


@st.cache_data(ttl=10)
def get_user_unique_leagues(username: str):

  return conn.query(f"SELECT DISTINCT(league_name) FROM {TABLE_BETS} WHERE user = '{username}'", ttl=600)


@st.cache_data(ttl=10)
def get_user_unique_bookmakers(username: str):

  return conn.query(f"SELECT DISTINCT(bookmaker) FROM {TABLE_BETS} WHERE user = '{username}'", ttl=600)


@st.cache_data(ttl=10)
def get_user_unique_tags(username: str):

  return conn.query(f"SELECT DISTINCT(tag) FROM {TABLE_BETS} WHERE user = '{username}'", ttl=600)
