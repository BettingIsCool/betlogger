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

  return conn.query(f"SELECT event_id, league_id, league_name, starts, runner_home, runner_away FROM {TABLE_FIXTURES} WHERE sport_id = {sport_id} AND DATE(starts) >= '{date_from.strftime('%Y-%m-%d')}' AND DATE(starts) <= '{date_to.strftime('%Y-%m-%d')}'", ttl=600)
