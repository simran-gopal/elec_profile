import subprocess
import sys
import os
import warnings
warnings.filterwarnings('ignore')

if os.path.exists('requirements.txt'):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])

import pandas as pd
import streamlit as st
import pandas.io.sql as sqlio
import json
import geopy.distance
import mysql.connector
import configparser
import reverse_geocoder as rg

config = configparser.ConfigParser()
config.read(r"mynzo_staging_config.ini")

mynzo_db_read = mysql.connector.connect(host=config['mynzo_db_read']['host'],
                                   user=config['mynzo_db_read']['user'],
                                   password=config['mynzo_db_read']['password'],
                                   database=config['mynzo_db_read']['database'], 
                                   connection_timeout=int(config['mynzo_db_read']['connection_timeout']))

geo_table = pd.read_sql_query('select id, code, latitude, longitude, parent_id from geo', mynzo_db_read)

st.title('Electric Profile Generator')

@st.cache
def load_data():
    return pd.read_sql_query('select occupation, email from user_setting us left join user u on us.user_id=u.id;', mynzo_db_read)

data_df = load_data()

a = st.text_input("Enter the Email:")
if len(a) > 2:
    if st.button('Generate Table'):
        occupation = data_df[data_df['email'].str.contains(a, case=False)]['occupation']
        mynzo_db_read.close()

        if not occupation.empty:
            st.write(f"Occupation for {a}: {occupation.iloc[0]}")
        else:
            st.write(f'There is no data for the email {a}')
else:
    st.write('Please enter a valid Email')
