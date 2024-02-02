import subprocess
import sys
import os
import warnings
warnings.filterwarnings('ignore')

if os.path.exists('requirements.txt'):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])

import pandas as pd
import streamlit as st
import mysql.connector
import configparser

config = configparser.ConfigParser()
config.read(r"mynzo_staging_config.ini")

mynzo_db_read = mysql.connector.connect(host=config['mynzo_db_read']['host'],
                                   user=config['mynzo_db_read']['user'],
                                   password=config['mynzo_db_read']['password'],
                                   database=config['mynzo_db_read']['database'], 
                                   connection_timeout=int(config['mynzo_db_read']['connection_timeout']))

# Fetch all columns initially
data_df = pd.read_sql_query('select occupation, email from user_setting us left join user u on us.user_id=u.id;', mynzo_db_read)

st.title('Occupation from email')

@st.cache_data(hash_funcs={mysql.connector.connection_cext.CMySQLConnection: lambda x: None})
def load_data():
    return data_df

a = st.text_input("Enter the Email:")
if len(a) > 2:
    # Check for NaN values before filtering
    filtered_data = data_df[data_df['email'].str.contains(a, case=False, na=False)]

    if not filtered_data.empty:
        st.write("Generated Table:")
        st.write(filtered_data)
    else:
        st.write(f'There is no data for the email {a}')
else:
    st.write('Please enter a valid Email')
