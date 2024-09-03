import time
import tools
import db_imr
import pandas as pd
import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt
import streamlit_authenticator as stauth

# Switch to wide-mode for better view
st.set_page_config(layout="wide")

# Add a bet
unique_sports = db_imr.get_sports()
