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

mynzo_db_read = mysql.connector.
