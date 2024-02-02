import subprocess
import sys
import os
import warnings
warnings.filterwarnings('ignore')
# Check if requirements.txt exists
if os.path.exists('requirements.txt'):
#     # Install dependencies from requirements.txt
#     try:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
    # except subprocess.CalledProcessError:
    #     print("Error installing dependencies from requirements.txt")

import pandas as pd
import streamlit as st
import pandas.io.sql as sqlio
import json
import geopy.distance
import mysql.connector
import configparser
import reverse_geocoder as rg

config = configparser.ConfigParser()

# config.read(r"C:\Users\simra\Downloads\python_scripts\cred_aws.txt")
config.read(r"mynzo_staging_config.ini")

mynzo_db_read = mysql.connector.connect(host=config['mynzo_db_read']['host'],
                                   user=config['mynzo_db_read']['user'],
                                   password=config['mynzo_db_read']['password'],
                                   database=config['mynzo_db_read']['database'], 
                                   connection_timeout=int(config['mynzo_db_read']['connection_timeout']))

geo_table = pd.read_sql_query('select id, code, latitude, longitude, parent_id from geo', mynzo_db_read)

# Streamlit app
st.title('Electric Profile Generator')

# User input
a= st.text_input("Enter the Email:")
if len(a)>2:
  # Generate table based on user input
    if st.button('Generate Table'):
        data_df = pd.read_sql_query(f'''select occupation from user_setting us left join user u on us.user_id=u.id where email like '%{a}%';''', mynzo_db_read)
        mynzo_db_read.close()
        csv_data = data_df.to_csv(index=False)
        st.download_button(label="Download Table as CSV",data=csv_data,file_name='generated_table.csv',key='download_button')
    else:
        st.write('There is no data for this Email')
    # else:
    #     st.write('There is no data for this lat long')
      
