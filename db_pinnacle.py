import streamlit as st
from sqlalchemy import text
from config import TABLE_SPORTS, TABLE_LEAGUES, TABLE_FIXTURES, TABLE_ODDS, TABLE_RESULTS, TABLE_BETS, TABLE_USERS

conn = st.connection('pinnacle', type='sql')


@st.cache_data(ttl=10)
def get_sports():

  return conn.query(f"SELECT DISTINCT(sport_name) FROM {TABLE_SPORTS}", ttl=600)['sport_name'].tolist()
