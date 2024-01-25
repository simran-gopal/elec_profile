# import warnings
# warnings.filterwarnings("ignore")
import pandas as pd
# import numpy as np
import streamlit as st
# import sshtunnel
# import paramiko
# from paramiko import SSHClient
# from sshtunnel import SSHTunnelForwarder
# import traceback
import pandas.io.sql as sqlio
# import psycopg2
import json
import geopy.distance
import mysql.connector
# from geopy.geocoders import Nominatim
# from statistics import mode
# import cv2
# import urllib
# import requests
# from PIL import ImageColor
# import traceback
# import h3
# from timezonefinder import TimezoneFinder
# from io import StringIO
# from itertools import chain
# from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
# import boto3
# import time
import configparser
import reverse_geocoder as rg
# import time
# import re
# import datetime
# from datetime import datetime, date, timedelta
# import pymysql


config = configparser.ConfigParser()

# config.read(r"C:\Users\simra\Downloads\python_scripts\cred_aws.txt")
config.read(r"C:\Users\simra\Downloads\python_scripts\mynzo_staging_config.ini")

iso_alpha2_to_alpha3 = {'AF': 'AFG', 'AX': 'ALA', 'AL': 'ALB', 'DZ': 'DZA', 'AS': 'ASM', 'AD': 'AND', 'AO': 'AGO', 'AI': 'AIA', 'AQ': 'ATA', 'AG': 'ATG', 'AR': 'ARG', 'AM': 'ARM', 'AW': 'ABW', 'AU': 'AUS', 'AT': 'AUT', 'AZ': 'AZE', 'BS': 'BHS', 'BH': 'BHR', 'BD': 'BGD', 'BB': 'BRB', 'BY': 'BLR', 'BE': 'BEL', 'BZ': 'BLZ', 'BJ': 'BEN', 'BM': 'BMU', 'BT': 'BTN', 'BO': 'BOL', 'BQ': 'BES', 'BA': 'BIH', 'BW': 'BWA', 'BV': 'BVT', 'BR': 'BRA', 'IO': 'IOT', 'BN': 'BRN', 'BG': 'BGR', 'BF': 'BFA', 'BI': 'BDI', 'CV': 'CPV', 'KH': 'KHM', 'CM': 'CMR', 'CA': 'CAN', 'KY': 'CYM', 'CF': 'CAF', 'TD': 'TCD', 'CL': 'CHL', 'CN': 'CHN', 'CX': 'CXR', 'CC': 'CCK', 'CO': 'COL', 'KM': 'COM', 'CD': 'COD', 'CG': 'COG', 'CK': 'COK', 'CR': 'CRI', 'CI': 'CIV', 'HR': 'HRV', 'CU': 'CUB', 'CW': 'CUW', 'CY': 'CYP', 'CZ': 'CZE', 'DK': 'DNK', 'DJ': 'DJI', 'DM': 'DMA', 'DO': 'DOM', 'EC': 'ECU', 'EG': 'EGY', 'SV': 'SLV', 'GQ': 'GNQ', 'ER': 'ERI', 'EE': 'EST', 'SZ': 'SWZ', 'ET': 'ETH', 'FK': 'FLK', 'FO': 'FRO', 'FJ': 'FJI', 'FI': 'FIN', 'FR': 'FRA', 'GF': 'GUF', 'PF': 'PYF', 'TF': 'ATF', 'GA': 'GAB', 'GM': 'GMB', 'GE': 'GEO', 'DE': 'DEU', 'GH': 'GHA', 'GI': 'GIB', 'GR': 'GRC', 'GL': 'GRL', 'GD': 'GRD', 'GP': 'GLP', 'GU': 'GUM', 'GT': 'GTM', 'GG': 'GGY', 'GN': 'GIN', 'GW': 'GNB', 'GY': 'GUY', 'HT': 'HTI', 'HM': 'HMD', 'VA': 'VAT', 'HN': 'HND', 'HK': 'HKG', 'HU': 'HUN', 'IS': 'ISL', 'IN': 'IND', 'ID': 'IDN', 'IR': 'IRN', 'IQ': 'IRQ', 'IE': 'IRL', 'IM': 'IMN', 'IL': 'ISR', 'IT': 'ITA', 'JM': 'JAM', 'JP': 'JPN', 'JE': 'JEY', 'JO': 'JOR', 'KZ': 'KAZ', 'KE': 'KEN', 'KI': 'KIR', 'KP': 'PRK', 'KR': 'KOR', 'KW': 'KWT', 'KG': 'KGZ', 'LA': 'LAO', 'LV': 'LVA', 'LB': 'LBN', 'LS': 'LSO', 'LR': 'LBR', 'LY': 'LBY', 'LI': 'LIE', 'LT': 'LTU', 'LU': 'LUX', 'MO': 'MAC', 'MG': 'MDG', 'MW': 'MWI', 'MY': 'MYS', 'MV': 'MDV', 'ML': 'MLI', 'MT': 'MLT', 'MH': 'MHL', 'MQ': 'MTQ', 'MR': 'MRT', 'MU': 'MUS', 'YT': 'MYT', 'MX': 'MEX', 'FM': 'FSM', 'MD': 'MDA', 'MC': 'MCO', 'MN': 'MNG', 'ME': 'MNE', 'MS': 'MSR', 'MA': 'MAR', 'MZ': 'MOZ', 'MM': 'MMR', 'NA': 'NAM', 'NR': 'NRU', 'NP': 'NPL', 'NL': 'NLD', 'NC': 'NCL', 'NZ': 'NZL', 'NI': 'NIC', 'NE': 'NER', 'NG': 'NGA', 'NU': 'NIU', 'NF': 'NFK', 'MK': 'MKD', 'MP': 'MNP', 'NO': 'NOR', 'OM': 'OMN', 'PK': 'PAK', 'PW': 'PLW', 'PS': 'PSE', 'PA': 'PAN', 'PG': 'PNG', 'PY': 'PRY', 'PE': 'PER', 'PH': 'PHL', 'PN': 'PCN', 'PL': 'POL', 'PT': 'PRT', 'PR': 'PRI', 'QA': 'QAT', 'RE': 'REU', 'RO': 'ROU', 'RU': 'RUS', 'RW': 'RWA', 'BL': 'BLM', 'SH': 'SHN', 'KN': 'KNA', 'LC': 'LCA', 'MF': 'MAF', 'PM': 'SPM', 'VC': 'VCT', 'WS': 'WSM', 'SM': 'SMR', 'ST': 'STP', 'SA': 'SAU', 'SN': 'SEN', 'RS': 'SRB', 'SC': 'SYC', 'SL': 'SLE', 'SG': 'SGP', 'SX': 'SXM', 'SK': 'SVK', 'SI': 'SVN', 'SB': 'SLB', 'SO': 'SOM', 'ZA': 'ZAF', 'GS': 'SGS', 'SS': 'SSD', 'ES': 'ESP', 'LK': 'LKA', 'SD': 'SDN', 'SR': 'SUR', 'SJ': 'SJM', 'SE': 'SWE', 'CH': 'CHE', 'SY': 'SYR', 'TW': 'TWN', 'TJ': 'TJK', 'TZ': 'TZA', 'TH': 'THA', 'TL': 'TLS', 'TG': 'TGO', 'TK': 'TKL', 'TO': 'TON', 'TT': 'TTO', 'TN': 'TUN', 'TR': 'TUR', 'TM': 'TKM', 'TC': 'TCA', 'TV': 'TUV', 'UG': 'UGA', 'UA': 'UKR', 'AE': 'ARE', 'GB': 'GBR', 'US': 'USA', 'UM': 'UMI', 'UY': 'URY', 'UZ': 'UZB', 'VU': 'VUT', 'VE': 'VEN', 'VN': 'VNM', 'VG': 'VGB', 'VI': 'VIR', 'WF': 'WLF', 'EH': 'ESH', 'YE': 'YEM', 'ZM': 'ZMB', 'ZW': 'ZWE'}

def dist_calc(coord1, coord2):
    '''Funtion to compute Geodesic Distance Between two coordinates'''
    dist = geopy.distance.geodesic(coord1, coord2).km
    return dist

def geo_id_finder(lat, lon, geo_table_):
   
    coordinates = lat,lon
    try:
        country_code = rg.get(coordinates, mode=1)['cc']
   
        geo_country_id  = geo_table_[geo_table_.code == 
                                    iso_alpha2_to_alpha3[country_code]]
        all_regions = geo_table_[geo_table_.parent_id.isin(list(geo_table_[geo_table_.parent_id == 
                                                                        geo_country_id.id.item()].id))]
        all_regions['int_lat'] = all_regions.apply(
            lambda x: int(x.latitude) 
            if x.latitude==x.latitude else x.latitude, axis=1)
        all_regions['int_lon'] = all_regions.apply(
            lambda x: int(x.longitude) 
            if x.longitude==x.longitude else x.longitude, axis=1)
        all_regions_filt = all_regions[(all_regions.int_lat == int(lat)) & (all_regions.int_lon == int(lon))]
        if all_regions_filt.shape[0]>0:
            all_regions_filt['distance'] = all_regions_filt.apply(
                lambda x:dist_calc((x.latitude, x.longitude), (lat, lon)), axis=1)
            geo_id  = all_regions_filt.sort_values(by = 'distance').head(1).id.item()
        else:
            if geo_country_id.id.item() != 'IND':
                all_regions_filt = all_regions[~pd.isna(all_regions.latitude)]
                if all_regions_filt.shape[0]>0:
                    all_regions_filt['distance'] = all_regions_filt.apply(
                        lambda x:dist_calc((x.latitude, x.longitude), (lat, lon)), axis=1)
                    geo_id  = all_regions_filt.sort_values(by = 'distance').head(1).id.item()   
                else:
                    geo_id = None
            else:    
                geo_id = None
    except:
        print('Country Not mapped')
        geo_id = None
    return geo_id

def flatten_dict(row_dict):
    flat_ls = [[level1,level2,level3,level4, value]
                 for level1, inner1 in json.loads(row_dict).items()
                 for level2, inner2 in inner1.items()
                 for level3, inner3 in inner2.items()
                 for level4, value in inner3.items()]
    return flat_ls

mynzo_db_read = mysql.connector.connect(host=config['mynzo_db_read']['host'],
                                   user=config['mynzo_db_read']['user'],
                                   password=config['mynzo_db_read']['password'],
                                   database=config['mynzo_db_read']['database'], 
                                   connection_timeout=int(config['mynzo_db_read']['connection_timeout']))

geo_table = pd.read_sql_query('select id, code, latitude, longitude, parent_id, holiday_details from geo', mynzo_db_read)
# Streamlit app
st.title('Electric Profile Generator')

# User input
a= st.text_input("Enter the lat long:")
if len(a)>2:
  a=a.split(',')
  lat = float(a[0])
  lon=float(a[1])
  
  # Generate table based on user input
  if st.button('Generate Table'):
      # Create a DataFrame based on user input
      # data = {'Value 1': [value1], 'Value 2': [value2]}
      # df = pd.DataFrame(data)
      geo_id=geo_id_finder(lat, lon, geo_table)
  
      data_df = pd.read_sql_query(f'''select lec.geo_id, lec.electricity_factor,  
      lec.base_lib_electric_consumption_id, lec.electricity_indus_per_cap, 
      lec.electricity_comm_per_cap, lec.electricity_resi_per_cap, 
      lec.gas_indus_per_cap, lec.gas_comm_per_cap, lec.gas_resi_per_cap, blec.electric_config, blec.gas_config 
      from  lib_electric_consumption lec
      inner join base_lib_electric_consumption blec on lec.base_lib_electric_consumption_id = blec.id 
      where lec.geo_id in ({geo_id});''', mynzo_db_read)
  
      mynzo_db_read.close()
  
      test = flatten_dict(data_df.electric_config[0])
      data_df['elec_ls'] =  data_df.electric_config.apply(lambda x: flatten_dict(x))
      data_df['gas_ls'] =  data_df.gas_config.apply(lambda x: flatten_dict(x))
      test = data_df.explode('elec_ls')
      test2 = data_df.explode('gas_ls')
      test2.drop(['electric_config', 'gas_config','elec_ls'], axis=1, inplace=True)
      test.drop(['electric_config', 'gas_config','gas_ls'], axis=1, inplace=True)
      test['gas_ls'] = test2.gas_ls
      test['building_type'] = test.elec_ls.apply(lambda x:x[0])
      test['month'] = test.elec_ls.apply(lambda x:x[1])
      test['day'] = test.elec_ls.apply(lambda x:x[2])
      test['hour'] = test.elec_ls.apply(lambda x:x[3])
      test['elec_value'] = test.elec_ls.apply(lambda x:x[4])
      test['gas_value'] = test.gas_ls.apply(lambda x:x[4])
      display=test[[ 'geo_id', 'electricity_factor',
             'electricity_indus_per_cap', 'electricity_comm_per_cap',
             'electricity_resi_per_cap', 'gas_indus_per_cap', 'gas_comm_per_cap',
             'gas_resi_per_cap', 'building_type', 'month',
             'day', 'hour', 'elec_value', 'gas_value']]
      
      # Display the generated table
      st.write('Generated Table:')
      # st.write(display)
      
      # Add a download button for the generated table
      csv_data = display.to_csv(index=False)
      st.download_button(
          label="Download Table as CSV",
          data=csv_data,
          file_name='generated_table.csv',
          key='download_button'
      )
