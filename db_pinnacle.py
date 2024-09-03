import streamlit as st
from sqlalchemy import text
from config import TABLE_FIXTURES, TABLE_ODDS, TABLE_RESULTS

conn = st.connection('imr', type='sql')


@st.cache_data(ttl=10)
def get_sports():

  return conn.query(f"SELECT DISTINCT(sport_name) FROM {TABLE_FIXTURES}", ttl=600)['sport_name'].tolist()
