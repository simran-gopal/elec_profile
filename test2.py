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

st.title('Electric Profile Generator')

a = st.text_input("Enter the Email:")
if len(a) > 2:
    data_df = pd.read_sql_query(f'''select occupation from user_setting us left join user u on us.user_id=u.id where email like '%{a}%';''', mynzo_db_read)
    mynzo_db_read.close()

    if not data_df.empty:
        st.write("Generated Table:")
        st.write(data_df)
    else:
        st.write('There is no data for this Email')
else:
    st.write('Please enter a valid Email')
