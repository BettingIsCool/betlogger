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

  return conn.query(f"SELECT period, market, line FROM {TABLE_ODDS} WHERE event_id = {event_id}", ttl=600)
