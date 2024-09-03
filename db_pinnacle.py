import streamlit as st
from sqlalchemy import text
from config import TABLE_LEAGUES, TABLE_FIXTURES, TABLE_ODDS, TABLE_RESULTS, TABLE_BETS, TABLE_USERS

conn = st.connection('pinnacle', type='sql')


@st.cache_data(ttl=10)
def get_leagues(sport_id: int):

  return conn.query(f"SELECT league_id, league_name FROM {TABLE_LEAGUES} WHERE sport_id = {sport_id}", ttl=600).todict()
