########################################### Import Libraries ###########################################
import warnings
warnings.filterwarnings("ignore")
import mysql.connector
import pymysql
import pandas as pd
import numpy as np
import time
import streamlit as st
time.clock = time.time
import mysql.connector
import re
import datetime
from datetime import datetime, date, timedelta
from io import StringIO
from itertools import chain
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
# import pymongo
import plotly
import json
from PIL import Image
import base64
import configparser
import io
import matplotlib.colors
import streamlit.components.v1 as components
from streamlit import session_state as ss
# from streamlit_float import *
import requests
config = configparser.ConfigParser()

if os.path.exists('requirements.txt'):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
image_path = r"images/mynzo_logo.png"

st.set_page_config(layout="wide", page_title="Workshop Analytics Dashboard",page_icon="🧊",)
float_init()

# Declares session variables.
setattr(ss, 'is_login', getattr(ss, 'is_login', False))
setattr(ss, 'err_msg', getattr(ss, 'err_msg', None))

html_time_reset = """
<html>
<head>
    <style>
    :root {background-color: #F0F2F6;}
    @import url('https://fonts.googleapis.com/css2?family=Nunito:ital,wght@0,200..1000;1,200..1000&display=swap');
        
        #time {
            color: #858585;
            font-family: 'Nunito', sans-serif;
            text-align: center;
        }
    </style>
</head>
<body>
<script>
    var lastReload = last_reload_time;

    function updateTime() {
        var currentTime = current_time;
        var timeDifference = currentTime - lastReload;
        var seconds = Math.floor((timeDifference % (1000 * 60)) / 1000);
        var minutes = Math.floor((timeDifference % (1000 * 60 * 60)) / (1000 * 60));

        document.getElementById("time").innerHTML = "Last Refreshed " + minutes + " mins. " + seconds + " secs. ago";
    }

    setInterval(updateTime, 1000);

    window.onload = function() {
        updateTime();
    }

    window.onbeforeunload = function(){
        lastReload = current_time;
    };
</script>

<div id="time">Time since last reload: 0 minutes 0 seconds</div>

</body>
</html>
"""


st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Nunito:ital,wght@0,200..1000;1,200..1000&display=swap');
        html, body, [class*="css"] {
            font-family: 'Nunito';
            font-color: #858585
        }
           .block-container {
                padding-top: 0.5rem;
                padding-bottom: 10rem;
                margin-top: -70px;}
           .css-1544g2n.e1fqkh3o4 {
                margin-top: -50px;}
            div.row-widget.stRadio > div {
             flex-direction: row;
             align-items: stretch;
            }

            div.row-widget.stRadio > div[role="radiogroup"] > label[data-baseweb="radio"]  {
             background-color: #A3D5E4;
             padding-right: 10px;
             padding-left: 4px;
             padding-bottom: 3px;
             margin: 4px;
            }
            .streamlit-expander {
                border: 3 !important;
                border-radius: 10px;
                color: black;}
            div[data-testid="stVerticalBlock"] div:has(div.fixed-header) {
                                position: sticky;
                                top: 2.875rem;
                                background-color: white;
                                z-index: 999;}
            .stApp a:first-child {
                display: none;
            }

            .css-15zrgzn {display: none}
            .css-eczf16 {display: none}
            .css-jn99sy {display: none}
            body {
                font-family: 'Nunito';
                font-color: #858585;}
                
        </style>

        """, unsafe_allow_html=True)

css_start = """
<!DOCTYPE html>
<html>
<head>
<link href='https://fonts.googleapis.com/css?family=Nunito' rel='stylesheet'>
<style>
table {
  border-collapse: separate;
  border-spacing: 0;
  width: 100%;
}
th, td {
  padding: 8px;
  text-align: left;
  border: 2px solid #ddd;
  border-radius: 10px;
  font-family: 'Nunito'
}

th {
  background-color: #f2f2f2;
  text-align: center;
}

td:hover {
  background-color: lightblue;
}

th:hover {
  background-color: lightblue;
}
</style>
</head>
<body>"""
css_end = """</body></html>"""
css_table_height = 600

sql_hostname = st.secrets["host"]
sql_username = st.secrets["user"]
sql_password = st.secrets["password"]
sql_main_database = st.secrets["database"]

mongo_client = pymongo.MongoClient(host=st.secrets["mongo_host"])
data_base = mongo_client[st.secrets["mongo_db"]]
# fip_url = st.secrets["fip_url"]
register_url = st.secrets["register_url"]
quiz_list_url = st.secrets["quiz_list_url"]

def quiz_list(quiz_list_url, choice):
    try:
        resp_quiz = requests.get(url = quiz_list_url.replace('workshop_choice', str(choice)))
        quiz_dict = resp_quiz.json() if resp_quiz.status_code==200 else None
        if pd.notna(quiz_dict):
            all_quizzes = [{'questionId':x['question_id'],'correct_answer':x['answer']} for x in quiz_dict['data'][0]['questions']]
        else:
            all_quizzes=None
    except:
        all_quizzes=None
    return all_quizzes

def bar_chart_maker(df, x_axis, y_axis, xaxis_title, yaxis_title,col_name, orient, new_col_names,color_map,category_order):
    if df.shape[0]==0:
        df=pd.DataFrame(np.zeros([1,len(df.columns)]),columns=df.columns)   
    fig = px.bar(df, y=y_axis, x=x_axis, text_auto=True, orientation='v', barmode='group', color_discrete_map=color_map, category_orders={x_axis: category_order})
    fig.update_traces(textfont_size=16, textangle=0, textposition="inside", cliponaxis=False, textfont_color="black")
    fig.update_layout(autosize=False,height=300,showlegend=True, margin=dict(l=0, r=0, t=10, b=0), font=dict(size=16, color='black',family="Nunito"), xaxis_title=xaxis_title, yaxis_title=yaxis_title)
    fig.update_xaxes(showline=False,linewidth=2,linecolor='#63316F',mirror=True,
                     tickfont=dict(size=16, color='black',family="Nunito"), title=dict(font=dict(size=16, color='black',family="Nunito")))
    fig.update_yaxes(showline=False,linewidth=2,linecolor='#63316F',mirror=True, tickangle = -90, 
                     tickfont=dict(size=16, color='black',family="Nunito"), title=dict(font=dict(size=16, color='black',family="Nunito")))
    fig.update_layout(legend=dict(title="Legends", font=dict(size=14, color='black',family="Nunito")))


    fig.for_each_trace(lambda t: t.update(name = new_col_names[t.name],
                                          legendgroup = new_col_names[t.name],
                                          hovertemplate = t.hovertemplate.replace(t.name, new_col_names[t.name])))
    col_name.plotly_chart(fig, theme="streamlit", use_container_width=True, config={'displayModeBar': False})
    

def calculate_metric_for_email(MQI_data, email_id, time_delta,workshop_participants, user_org_data):
    filt_data = MQI_data[(MQI_data.frequency=='daily')&
    (MQI_data.workshop_email==email_id)]
    owner_id = workshop_participants[workshop_participants.workshop_email == email_id].workshop_user_id.item() if len(workshop_participants[workshop_participants.workshop_email == email_id].workshop_user_id)==1 else None
    if time_delta==0:
        filt_data['summation'] = filt_data.emission-filt_data.individual_credit-filt_data.enterprise_credit
        filt_data['date']=pd.to_datetime(filt_data['date'])
        result = filt_data[(filt_data.date>=(pd.Timestamp.utcnow()-pd.Timedelta(days=91)).strftime('%Y-%m-%d %H:%M')) & ((filt_data.date<=(pd.Timestamp.utcnow()+pd.Timedelta(days=0)).strftime('%Y-%m-%d %H:%M')))].drop_duplicates(subset='date',keep='last').summation.sum()/filt_data[(filt_data.date>=(pd.Timestamp.utcnow()-pd.Timedelta(days=91)).strftime('%Y-%m-%d %H:%M')) & ((filt_data.date<=(pd.Timestamp.utcnow()+pd.Timedelta(days=0)).strftime('%Y-%m-%d %H:%M')))].drop_duplicates(subset='date',keep='last').ideal_emission.sum()*100

    elif time_delta==90:
        if filt_data[filt_data.date>pd.Timestamp.utcnow().strftime("%Y-%m-%d")].shape[0]>0:
            if bool(owner_id):
                if user_org_data[user_org_data.workshop_user_id == owner_id].shape[0]>0:
                    per_employee_unit_allocation = (user_org_data[user_org_data.workshop_user_id == owner_id].per_employee_unit_allocation.item())
                else:
                    per_employee_unit_allocation=0
                if not bool(per_employee_unit_allocation):
                    per_employee_unit_allocation=0
                per_employee_unit_allocation = per_employee_unit_allocation/365
                filt_data_past = filt_data[(filt_data.date>=(pd.Timestamp.utcnow()-pd.DateOffset(months=2)).strftime('%Y-%m-01')) & (filt_data.date<=pd.Timestamp.utcnow().strftime('%Y-%m-%d'))]
                filt_data_future = filt_data[((filt_data.date>pd.Timestamp.utcnow().strftime('%Y-%m-%d'))) & ((filt_data.date<=(pd.Timestamp((pd.Timestamp.utcnow()-pd.DateOffset(months=2)+pd.DateOffset(months=6)).strftime('%Y-%m-01'))-pd.Timedelta(days=1)).strftime('%Y-%m-%d')))].drop_duplicates(subset='date',keep='last')
                filt_data_past['summation'] = filt_data_past.emission-filt_data_past.individual_credit
                filt_data_future['summation'] = filt_data_future.emission-filt_data_future.individual_credit-per_employee_unit_allocation
                filt_data_all = pd.concat([filt_data_past,filt_data_future], axis=0)
                filt_data_all['date']=pd.to_datetime(filt_data_all['date'])
                result = filt_data_all.drop_duplicates(subset='date',keep='last').summation.sum()/filt_data_all.drop_duplicates(subset='date',keep='last').ideal_emission.sum()*100
            else:
                result= None
        else:
            result=None
    return result


def mqi_2030(email,workshop_emails_,workshop_participants,MQI_data,seques_plan,user_org_data):
    workshop_emails_ = workshop_emails_.drop('workshop_user_id', axis=1).merge(workshop_participants, on='workshop_email', how='left').drop_duplicates(subset=['workshop_email'], keep='first')
    owner_id = workshop_emails_[workshop_emails_.workshop_email == email].workshop_user_id.item() if len(workshop_emails_[workshop_emails_.workshop_email == email].workshop_user_id)==1 else None
    if bool(owner_id):
        if user_org_data[user_org_data.workshop_user_id == owner_id].shape[0]>0:
            per_employee_unit_allocation = user_org_data[user_org_data.workshop_user_id == owner_id].per_employee_unit_allocation.item()
        else:
            per_employee_unit_allocation=0
        if not bool(per_employee_unit_allocation):
            per_employee_unit_allocation=0
        if owner_id in  [x for x in seques_plan.owner_id]:
            paid_sip = seques_plan[seques_plan.owner_id == owner_id].drop_duplicates(subset=['owner_id'],keep='last').paid_sip.item()
            is_active = seques_plan[seques_plan.owner_id == owner_id].drop_duplicates(subset=['owner_id'],keep='last').is_active.item()
            total_sip = seques_plan[seques_plan.owner_id == owner_id].drop_duplicates(subset=['owner_id'],keep='last').total_sip.item()
            sip_area = seques_plan[seques_plan.owner_id == owner_id].drop_duplicates(subset=['owner_id'],keep='last').sip_area.item()           
            if (paid_sip>1 and is_active==0):         
                total_credit = (sip_area * 3 * 12 * 30 * 2400000) / (500 * 365)
            elif paid_sip==total_sip:
                total_credit = sum([(sip_area * month * 30 * 2400000) / (500 * 365) for month in range(paid_sip - 11, paid_sip + 1)])
            else:
                total_credit =0
        else:
            total_credit =0

        if MQI_data[(MQI_data.workshop_user_id==owner_id) & (MQI_data.frequency=='yearly') & (MQI_data['date']=='2030')].drop_duplicates(subset=['workshop_user_id']).shape[0]>0:
            mqi = (MQI_data[(MQI_data.workshop_user_id==owner_id) & (MQI_data.frequency=='yearly') & (MQI_data['date']=='2030')].drop_duplicates(subset=['workshop_user_id']).emission.item() - MQI_data[(MQI_data.workshop_user_id==owner_id) & (MQI_data.frequency=='yearly') & (MQI_data['date']=='2030')].drop_duplicates(subset=['workshop_user_id']).individual_credit.item() -(total_credit+per_employee_unit_allocation))*100/MQI_data[(MQI_data.workshop_user_id==owner_id) & (MQI_data.frequency=='yearly') & (MQI_data['date']=='2030')].drop_duplicates(subset=['workshop_user_id']).ideal_emission.item()
        else:
            mqi=None
    else:
        mqi=None        
    return mqi
    
# @st.cache_data(show_spinner=True,ttl=60)
def data_fetch():
#     mynzo_db_read = pymysql.connect(host=sql_hostname, user=sql_username,
#                            passwd=sql_password, db=sql_main_database)
    
    
#     MQI_data = pd.read_sql_query(f'''select wu.workshop_id, cu.mqi,cu.frequency, cu.date, wu.workshop_user_id, cu.emission, 
#     cu.ideal_emission, cu.individual_credit, cu.enterprise_credit   
#     from workshop_user wu
#     inner join workshop w on wu.workshop_id = w.id
#     inner join user u on workshop_user_id = u.id
#     inner join cumulative_emissions cu on u.id = cu.user_id
#     where w.id={choice};''', mynzo_db_read)
    
#     mynzo_db_read.close()

    MQI_data = pd.DataFrame([x for x in data_base.mqi_data.find({'workshop_id':choice})]).drop('_id', axis=1, errors='ignore')    
    
    work_nudges = pd.DataFrame([x for x in data_base.work_nudges.find({'workshop_id':choice})]).drop('_id', axis=1, errors='ignore')
    work_quiz = pd.DataFrame([x for x in data_base.quizzes.find({'workshop_id':choice})]).drop('_id', axis=1, errors='ignore')
    workshop_emails = pd.DataFrame([x for x in data_base.workshop_emails.find({'workshop_id':choice})]).drop('_id', axis=1, errors='ignore')
    user_details = pd.DataFrame([x for x in data_base.user_details.find({'workshop_id':choice})]).drop('_id', axis=1, errors='ignore')
        
    if workshop_emails.shape[0]==0:
        seques_plan= pd.DataFrame(columns=['owner_id', 'total_amount', 'sip_amount', 'total_area', 'sip_area','net_zero_date', 'start_date', 'is_active', 'paid_sip', 'total_sip'])
    else:
        seques_plan = pd.DataFrame([x for x in 
                                    data_base.seques_plan.find({"owner_id":{"$in":[int(x) for x in workshop_emails.workshop_user_id.unique()]}})]).drop('_id', axis=1, errors='ignore')
    
    user_org_data = pd.DataFrame([x for x in data_base.user_org_data.find({'workshop_id':choice})]).drop('_id', axis=1, errors='ignore')
    workshop_fip = pd.DataFrame([x for x in data_base.workshop_fip.find({'workshop_id':choice})]).drop('_id', axis=1, errors='ignore')
    
    return work_nudges, work_quiz, MQI_data, workshop_emails, seques_plan, user_details, user_org_data, workshop_fip
    
def workshop_analytics(all_quizzes):
    
    work_nudges, work_quiz, MQI_data, workshop_emails, seques_plan, user_details, user_org_data, workshop_fip = data_fetch()
    # work_nudges = work_quiz = MQI_data = workshop_emails = seques_plan = user_details = user_org_data = workshop_fip= pd.DataFrame()

    if work_nudges.shape[0]==0:
        work_nudges = pd.DataFrame(columns=['workshop_id', 'workshop_user_id', 'nudges'])
    if work_quiz.shape[0]==0:
        work_quiz = pd.DataFrame(columns=['workshop_id', 'workshop_user_id', 'quiz_responses'])        
    if MQI_data.shape[0]==0:
        MQI_data = pd.DataFrame(columns=['workshop_id', 'mqi', 'frequency', 'date', 'workshop_user_id',
       'emission', 'ideal_emission', 'individual_credit', 'enterprise_credit'])
    if workshop_emails.shape[0]==0:
        workshop_emails = pd.DataFrame(columns=['workshop_id', 'workshop_email', 'name', 'original_email',
       'workshop_user_id'])
    if seques_plan.shape[0]==0:
        seques_plan= pd.DataFrame(columns=['owner_id', 'total_amount', 'sip_amount', 'total_area', 'sip_area','net_zero_date', 'start_date', 'is_active', 'paid_sip', 'total_sip'])    
    if user_details.shape[0]==0:
        user_details = pd.DataFrame(columns=['workshop_id', 'workshop_user_id', 'organization', 'department',
       'work_location', 'division'])
    if user_org_data.shape[0]==0:
        user_org_data = pd.DataFrame(columns=['workshop_id', 'workshop_user_id', 'per_employee_unit_allocation'])
    if workshop_fip.shape[0]==0:
        workshop_fip = pd.DataFrame(columns=['workshop_id', 'workshop_user_id', 'base_fip', 'after_nudge_fip'])
        
    workshop_fip[['base_fip', 'after_nudge_fip']] = workshop_fip[['base_fip', 'after_nudge_fip']].astype('float')
        
        
    workshop_emails = workshop_emails.drop_duplicates(subset='workshop_email', keep='first')   
    MQI_data = MQI_data.drop_duplicates()        
    work_nudges.nudges = work_nudges.nudges.apply(json.loads)
    work_quiz.quiz_responses = work_quiz.quiz_responses.apply(json.loads)
    seques_plan = seques_plan.drop_duplicates(subset=['owner_id', 'paid_sip', 'is_active'], keep='first').reset_index().drop('index', axis=1)
    workshop_participants = workshop_emails[['workshop_user_id', 'workshop_email']].copy()
    MQI_data = MQI_data.merge(workshop_emails[['workshop_email','name', 'original_email', 'workshop_user_id' ]], on='workshop_user_id')
    # workshop_participants = workshop_emails[['workshop_user_id', 'workshop_email']].copy()
    workshop_emails = MQI_data.groupby(by = 'workshop_email').agg({'workshop_user_id':'nunique'}).reset_index()
    workshop_emails['past_MQI'] = workshop_emails.workshop_email.apply(lambda x:calculate_metric_for_email(MQI_data, x, 0, workshop_participants, user_org_data))
    workshop_emails['future_MQI'] = workshop_emails.workshop_email.apply(lambda x:calculate_metric_for_email(MQI_data, x, 90, workshop_participants, user_org_data))
           
    workshop_emails['future_MQI'] = workshop_emails.apply(lambda x:x.future_MQI if x.future_MQI!=x.past_MQI else None, axis=1).replace(np.nan, None)
    workshop_emails_ = workshop_emails.copy()
    workshop_emails['for_2030']=workshop_emails.workshop_email.apply(lambda x:mqi_2030(x,workshop_emails_,workshop_participants,MQI_data,seques_plan, user_org_data)).replace(np.nan, None)
    workshop_emails[['past_range', 'future_range', 'range_2030']] = None
    workshop_emails['past_range'][workshop_emails.past_MQI.between(-3000,0)] = 'Less than 0'
    workshop_emails['past_range'][workshop_emails.past_MQI.between(0.00001,50)] = '0 to 50'
    workshop_emails['past_range'][workshop_emails.past_MQI.between(50,100)] = '50 to 100'
    workshop_emails['past_range'][workshop_emails.past_MQI.between(100,200)] = '100 to 200'
    workshop_emails['past_range'][workshop_emails.past_MQI.between(200,10000)] = '200 and above'
    workshop_emails['future_range'][workshop_emails.future_MQI.between(-3000,0)] = 'Less than 0'
    workshop_emails['future_range'][workshop_emails.future_MQI.between(0.00001,50)] = '0 to 50'
    workshop_emails['future_range'][workshop_emails.future_MQI.between(50,100)] = '50 to 100'
    workshop_emails['future_range'][workshop_emails.future_MQI.between(100,200)] = '100 to 200'
    workshop_emails['future_range'][workshop_emails.future_MQI.between(200,10000)] = '200 and above'
    workshop_emails['range_2030'][workshop_emails.for_2030.between(-3000,0)] = 'Less than 0'
    workshop_emails['range_2030'][workshop_emails.for_2030.between(0.00001,50)] = '0 to 50'
    workshop_emails['range_2030'][workshop_emails.for_2030.between(50,100)] = '50 to 100'
    workshop_emails['range_2030'][workshop_emails.for_2030.between(100,200)] = '100 to 200'
    workshop_emails['range_2030'][workshop_emails.for_2030.between(200,10000)] = '200 and above'
    workshop_emails = pd.merge(workshop_emails, MQI_data.drop_duplicates(subset=['workshop_email','name'])[['workshop_email','name']], on='workshop_email', how='left') 

    cur_dict ={'INR (₹)': 
           [{'range':[0,500],'text':'0 to 500'},
            {'range':[500,1000],'text':'500 to 1000'},
            {'range':[1000,2000],'text':'1000 to 2000'},
            {'range':[2000,100000],'text':'2000 and above'}],
           'USD ($)':  
           [{'range':[0,5],'text':'0 to 5'},
            {'range':[5,10],'text':'5 to 10'},
            {'range':[10,20],'text':'10 to 20'},
            {'range':[20,10000],'text':'20 and above'}]}

    category_order = ['0 to 500', '500 to 1000', '1000 to 2000', '2000 and above']
    category_order_mqi = ['Less than 0','0 to 50', '50 to 100', '100 to 200', '200 and above']
    
    if currency_choice == 'USD ($)':
        seques_plan.sip_amount =seques_plan.sip_amount/85
        category_order = ['0 to 5', '5 to 10', '10 to 20', '20 and above']
    
    plan_purchase = seques_plan.drop_duplicates(subset=['owner_id'], keep='first')
    plan_purchase = plan_purchase[~(plan_purchase.total_sip!=((pd.Timestamp('2030-12-01').year - pd.Timestamp.now().year) * 12 + pd.Timestamp('2030-12-01').month - pd.Timestamp.now().month))]
    plan_purchase_future =  seques_plan.drop_duplicates(subset=['owner_id'], keep='last')[(seques_plan.paid_sip ==3) | (seques_plan.paid_sip ==1)]
    plan_cancelled = seques_plan[(seques_plan.total_sip!=((pd.Timestamp('2030-12-01').year - pd.Timestamp.now().year) * 12 + pd.Timestamp('2030-12-01').month - pd.Timestamp.now().month))]
    plan_purchase_2030 = seques_plan[(seques_plan.paid_sip==seques_plan.total_sip) & ~(seques_plan.total_sip!=((pd.Timestamp('2030-12-01').year - pd.Timestamp.now().year) * 12 + pd.Timestamp('2030-12-01').month - pd.Timestamp.now().month))]
    plan_purchase['purchase_1'], plan_purchase_future['purchase_1'], plan_cancelled['purchase_1'],plan_purchase_2030['purchase_1'] = None, None, None, None
    plan_purchase['purchase_1'][plan_purchase.sip_amount.between(cur_dict[currency_choice][0]['range'][0], cur_dict[currency_choice][0]['range'][1])] = cur_dict[currency_choice][0]['text']
    plan_purchase['purchase_1'][plan_purchase.sip_amount.between(cur_dict[currency_choice][1]['range'][0], cur_dict[currency_choice][1]['range'][1])] = cur_dict[currency_choice][1]['text']
    plan_purchase['purchase_1'][plan_purchase.sip_amount.between(cur_dict[currency_choice][2]['range'][0], cur_dict[currency_choice][2]['range'][1])] = cur_dict[currency_choice][3]['text']
    plan_purchase['purchase_1'][plan_purchase.sip_amount.between(cur_dict[currency_choice][3]['range'][0], cur_dict[currency_choice][3]['range'][1])] = cur_dict[currency_choice][3]['text'] 
    
    plan_purchase_future['purchase_1'][plan_purchase_future.sip_amount.between(cur_dict[currency_choice][0]['range'][0], cur_dict[currency_choice][0]['range'][1])] = cur_dict[currency_choice][0]['text']
    plan_purchase_future['purchase_1'][plan_purchase_future.sip_amount.between(cur_dict[currency_choice][1]['range'][0], cur_dict[currency_choice][1]['range'][1])] = cur_dict[currency_choice][1]['text']
    plan_purchase_future['purchase_1'][plan_purchase_future.sip_amount.between(cur_dict[currency_choice][2]['range'][0], cur_dict[currency_choice][2]['range'][1])] = cur_dict[currency_choice][2]['text']
    plan_purchase_future['purchase_1'][plan_purchase_future.sip_amount.between(cur_dict[currency_choice][3]['range'][0], cur_dict[currency_choice][3]['range'][1])] = cur_dict[currency_choice][3]['text']  
    
    plan_cancelled['purchase_1'][plan_cancelled.sip_amount.between(cur_dict[currency_choice][0]['range'][0], cur_dict[currency_choice][0]['range'][1])] = cur_dict[currency_choice][0]['text']
    plan_cancelled['purchase_1'][plan_cancelled.sip_amount.between(cur_dict[currency_choice][1]['range'][0], cur_dict[currency_choice][1]['range'][1])] = cur_dict[currency_choice][1]['text']
    plan_cancelled['purchase_1'][plan_cancelled.sip_amount.between(cur_dict[currency_choice][2]['range'][0], cur_dict[currency_choice][2]['range'][1])] = cur_dict[currency_choice][2]['text']
    plan_cancelled['purchase_1'][plan_cancelled.sip_amount.between(cur_dict[currency_choice][3]['range'][0], cur_dict[currency_choice][3]['range'][1])] = cur_dict[currency_choice][3]['text']  
    
    plan_purchase_2030['purchase_1'][plan_purchase_2030.sip_amount.between(cur_dict[currency_choice][0]['range'][0], cur_dict[currency_choice][0]['range'][1])] = cur_dict[currency_choice][0]['text']
    plan_purchase_2030['purchase_1'][plan_purchase_2030.sip_amount.between(cur_dict[currency_choice][1]['range'][0], cur_dict[currency_choice][1]['range'][1])] = cur_dict[currency_choice][1]['text']
    plan_purchase_2030['purchase_1'][plan_purchase_2030.sip_amount.between(cur_dict[currency_choice][2]['range'][0], cur_dict[currency_choice][2]['range'][1])] = cur_dict[currency_choice][2]['text']
    plan_purchase_2030['purchase_1'][plan_purchase_2030.sip_amount.between(cur_dict[currency_choice][3]['range'][0], cur_dict[currency_choice][3]['range'][1])] = cur_dict[currency_choice][3]['text'] 
    work_nudges_ = pd.concat([work_nudges,pd.json_normalize(work_nudges.nudges)], axis=1)
    
    st.markdown(f"<h3 style='text-align: center; color: {primary_font_color}; font-family: Nunito;'></h3>", unsafe_allow_html=True)
    pil_image = Image.open(image_path).resize((87,25))
    img_bytes = io.BytesIO()
    pil_image.save(img_bytes, format='PNG')
    img_bytes = img_bytes.getvalue()
    img_base64 = base64.b64encode(img_bytes).decode()
    markdown_str = (
        f'<div style="display: flex; align-items: center; justify-content: center; width: 100%;">'
        f'<div style="text-align: center; width: 100%; margin: 0; padding: 0;"><h4 style="color: {primary_font_color}; font-family: Nunito; margin: 0; padding: 0;"><ins>{workshop_choice}</b></ins></h4></div>'
        f'<div style="color: {primary_font_color}; position:absolute;right:0;top:3px; font-size: 10px; opacity: 1"><p>Total Participants: {len(workshop_participants.workshop_email.unique())}</p></div>'
        f'<div style="position:absolute;left:0;top:7px"><img src="data:image/png;base64,{img_base64}" style="vertical-align: middle;"></div>'
        f'</div>' )

    header = st.container()
    header.markdown(markdown_str, unsafe_allow_html=True)
    header.write("""<div class='fixed-header'/>""", unsafe_allow_html=True)
    
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown(f"<h5 style='text-align: left; color: {primary_font_color}; font-family: Nunito;'>MQI and FIP Variations</h5>", unsafe_allow_html=True)
    
    with st.expander(""):
        col1,col2 = st.columns(2)
        st.markdown(f"<h5 style='text-align: left; color: {primary_font_color}; font-family: Nunito;'>MQI variation for the Workshop participants</h5>", unsafe_allow_html=True)
        color_map = {'past': '#A3D5E4','future': '#25ACD1','future_2030': '#454545'}
        
        bar_chart_maker(pd.DataFrame(workshop_emails.past_range.value_counts()).reset_index().rename(columns = {'count':'past'}).merge(pd.DataFrame(workshop_emails.future_range.value_counts()).reset_index().rename(columns = {'count': 'future', 'future_range':'past_range'}), on='past_range', how='outer').merge(pd.DataFrame(workshop_emails.range_2030.value_counts()).reset_index().rename(columns = {'count': 'future_2030', 'range_2030':'past_range'}), on='past_range', how='outer'), 'past_range', ['past', 'future', 'future_2030'], "MQI Ranges", "User Count", st, 'v', {'past':'For past 90 days', 'future':'Six Months', 'future_2030':'For 2030'}, color_map, category_order_mqi)
            
        st.markdown('<br>', unsafe_allow_html=True)
        st.markdown(f"<h5 style='text-align: left; color: {primary_font_color}; font-family: Nunito;'>FIP variation for the Workshop participants</h5>", unsafe_allow_html=True)

        if currency_choice == 'USD ($)':
            
            workshop_fip.base_fip =workshop_fip.base_fip/85
            workshop_fip.after_nudge_fip =workshop_fip.after_nudge_fip/85
            category_order = ['0 to 5', '5 to 10', '10 to 20', '20 and above']

        workshop_fip[['base','post_nudge']]=None
        workshop_fip['base'][workshop_fip.base_fip.between(cur_dict[currency_choice][0]['range'][0], cur_dict[currency_choice][0]['range'][1])] = cur_dict[currency_choice][0]['text']
        workshop_fip['base'][workshop_fip.base_fip.between(cur_dict[currency_choice][1]['range'][0], cur_dict[currency_choice][1]['range'][1])] = cur_dict[currency_choice][1]['text']
        workshop_fip['base'][workshop_fip.base_fip.between(cur_dict[currency_choice][2]['range'][0], cur_dict[currency_choice][2]['range'][1])] = cur_dict[currency_choice][2]['text']
        workshop_fip['base'][workshop_fip.base_fip.between(cur_dict[currency_choice][3]['range'][0], cur_dict[currency_choice][3]['range'][1])] = cur_dict[currency_choice][3]['text']

        workshop_fip['post_nudge'][workshop_fip.after_nudge_fip.between(cur_dict[currency_choice][0]['range'][0], cur_dict[currency_choice][0]['range'][1])] = cur_dict[currency_choice][0]['text']
        workshop_fip['post_nudge'][workshop_fip.after_nudge_fip.between(cur_dict[currency_choice][1]['range'][0], cur_dict[currency_choice][1]['range'][1])] = cur_dict[currency_choice][1]['text']
        workshop_fip['post_nudge'][workshop_fip.after_nudge_fip.between(cur_dict[currency_choice][2]['range'][0], cur_dict[currency_choice][2]['range'][1])] = cur_dict[currency_choice][2]['text']
        workshop_fip['post_nudge'][workshop_fip.after_nudge_fip.between(cur_dict[currency_choice][3]['range'][0], cur_dict[currency_choice][3]['range'][1])] = cur_dict[currency_choice][3]['text']
        workshop_fip_ = workshop_fip[['workshop_user_id','post_nudge']].copy()
        workshop_fip_ = workshop_fip_.rename(columns = {'post_nudge':'base'})
        workshop_fip.replace(np.nan, None)

        color_map = {'user_count_1': '#A3D5E4','user_count_2': '#454545'}
        bar_chart_maker(pd.DataFrame(workshop_fip.base.value_counts().reset_index().rename(columns={'count': 'user_count_1'})).merge(pd.DataFrame(workshop_fip_.base.value_counts().reset_index().rename(columns={'count': 'user_count_2'})), on ='base', how='outer'), 'base', ['user_count_1', 'user_count_2'], f"FIP Amount Ranges (in {currency_choice})", "Participant Count", st, 'v', {'user_count_1':'Base FIP', 'user_count_2':'Post Nudge FIP'}, color_map, category_order)
 
    df_nudges = pd.DataFrame({
                            'Flights':len([x for x in work_nudges_.reducedFlight if x!=-1]) 
                                      if 'reducedFlight' in work_nudges_.columns else 0,
                             'Car Pool':len([x for x in work_nudges_.carPool if x==True]) 
                                      if 'carPool' in work_nudges_.columns else 0,
                             'Public Transport':len([x for x in work_nudges_.publicTransport if x==True]) 
                                      if 'publicTransport' in work_nudges_.columns else 0,
                             'L.E.D':len([x for x in work_nudges_.led if x==True]) 
                                      if 'led' in work_nudges_.columns else 0,
                             'Solar Roof':len([x for x in work_nudges_.solarRoof if x!=-1]) 
                                      if 'solarRoof' in work_nudges_.columns else 0,
                             'Green Roof':len([x for x in work_nudges_.greenRoof if x==True]) 
                                      if 'greenRoof' in work_nudges_.columns else 0,
                             'Heat Pump':len([x for x in work_nudges_.heatPump if x==True]) 
                                      if 'heatPump' in work_nudges_.columns else 0},
                             index=[0]).T.reset_index().rename(columns={'index':'Nudges',0:'values'})

    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown(f"<h5 style='text-align: left; color: {primary_font_color}; font-family: Nunito;'>Your Nudges</h5>", unsafe_allow_html=True)
    with st.expander(""):     
        fig =px.bar(df_nudges, x='Nudges', y='values',barmode="group", color='Nudges', color_discrete_sequence =['#9ac7d4', '#90b8c4', '#87aab4', '#7d9ba4', '#748d94', '#6b7f85', '#617075', '#586265', '#4e5355', '#454545'][::-1][:df_nudges.shape[0]])
        fig.update_layout(yaxis_range=[0,work_nudges_.shape[0]])
        fig.update_traces(textfont_size=16, textangle=0, textposition="inside", cliponaxis=False, textfont_color="black")
        fig.update_layout(autosize=False,height=300, margin=dict(l=0, r=0, t=10, b=0), font=dict(size=16, color='black',family="Nunito"), xaxis_title='Nudges', yaxis_title='User Count')
        fig.update_xaxes(showline=False,linewidth=2,linecolor='#63316F',mirror=True,
                         tickfont=dict(size=16, color='black',family="Nunito"), title=dict(font=dict(size=16, color='black',family="Nunito")))
        fig.update_yaxes(showline=False,linewidth=2,linecolor='#63316F',mirror=True, tickangle = -90, 
                         tickfont=dict(size=16, color='black',family="Nunito"), title=dict(font=dict(size=16, color='black',family="Nunito")))
        st.plotly_chart(fig, theme="streamlit", use_container_width=True, config={'displayModeBar': False})
    
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown(f"<h5 style='text-align: left; color: {primary_font_color}; font-family: Nunito;'>Forest Purchase</h5>", unsafe_allow_html=True)
    with st.expander(""):
        fig = px.bar(pd.DataFrame([['Purchased Plan','Before Nudge',len(plan_purchase.owner_id.unique())],
        ['Updated/Continued Plan','After Nudge',len(plan_purchase_2030.owner_id.unique())],
         ['','After Nudge',len(plan_purchase_future.owner_id.unique())],
        ['Purchased Newly','After Nudge',len(plan_cancelled.owner_id.unique())]], columns=['sections', 'nudge', 'value']), x="nudge", y="value", color="sections", text_auto=True, color_discrete_map = {
            'Purchased Plan': '#A3D5E4',
            'Updated/Continued Plan': '#25ACD1',
            '': '#FFFFFF',
            'Purchased Newly': '#454545'})
        fig.update_layout(yaxis_range=[0,work_nudges_.shape[0]])
        fig.update_traces(textfont_size=16, textangle=0, textposition="inside", cliponaxis=False, textfont_color="black")
        fig.update_layout(autosize=False,height=300, margin=dict(l=0, r=0, t=10, b=0), font=dict(size=16, color='black',family="Nunito"), xaxis_title='Nudges', yaxis_title='Participant Count')
        fig.update_xaxes(showline=False,linewidth=2,linecolor='#63316F',mirror=True,
                         tickfont=dict(size=16, color='black',family="Nunito"), title=dict(font=dict(size=16, color='black',family="Nunito")))
        fig.update_yaxes(showline=False,linewidth=2,linecolor='#63316F',mirror=True, tickangle = -90, 
                         tickfont=dict(size=16, color='black',family="Nunito"), title=dict(font=dict(size=16, color='black',family="Nunito")))
        st.plotly_chart(fig, theme="streamlit", use_container_width=True, config={'displayModeBar': False})

    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown(f"<h5 style='text-align: left; color: {primary_font_color}; font-family: Nunito;'>Quiz Responses</h5>", unsafe_allow_html=True)
    
    
    with st.expander(""):

        if not isinstance(all_quizzes, list):
            all_quizzes=[{'questionId': None,'correct_answer': False}]
        mid_quiz_df = work_quiz.apply(
            lambda y:pd.DataFrame(all_quizzes).merge(pd.DataFrame(y.quiz_responses['answers']), 
                                                     on='questionId', 
                                                     how='left').replace(np.nan,'Not Attempted').apply(
                lambda x: [x.questionId,'Correct' 
                           if x.correct_answer == x.answer 
                           else 'Not attempted' 
                           if x.answer == 'Not Attempted' 
                           else 'InCorrect'], axis=1).to_list(), axis=1)
        if mid_quiz_df.shape[0]>0:
            quiz_df = pd.DataFrame(mid_quiz_df.explode().to_list(), 
                                       columns = ['question', 'resp']).pivot_table(
                    index='question',columns = 'resp', 
                    aggfunc = {'resp':'count'}).reset_index().replace(np.nan, 0)
            quiz_df.columns =[y.replace(', ','').replace('resp','') for y in [', '.join(pair) for pair in quiz_df.columns]]
        else:
            quiz_df = pd.DataFrame(columns =['question', 'Correct', 'InCorrect', 'Not attempted'])
        
        if isinstance(all_quizzes, list) and len(all_quizzes)>1:
            quiz_df_ =pd.DataFrame(all_quizzes).reset_index().rename(columns={'questionId':'question', 'index':'q_name'})
        else:
            quiz_df_ =pd.DataFrame(columns =['question', 'q_name','correct_answer'])
            
        quiz_df_.q_name =[f'Q{x+1}' for x in quiz_df_.q_name]
        quiz_plot_df =quiz_df.merge(quiz_df_[['question', 'q_name', 'correct_answer']], on='question', how='inner').drop('question', axis=1).rename(columns ={'q_name':'question'})
        
        if quiz_plot_df.shape[0]==0:
            quiz_plot_df = pd.DataFrame(np.zeros((1,5)), columns =['question', 'Correct', 'InCorrect', 'Not attempted', 'correct_answer'] )
            
        columns_to_check = ['question', 'Correct', 'InCorrect','Not attempted', 'correct_answer']
        if not all(x in quiz_plot_df.columns for x in columns_to_check):
            quiz_plot_df =[quiz_plot_df.assign(**{col: 0}) for col in columns_to_check if col not in quiz_plot_df.columns][0]
        
        quiz_plot_df['Not attempted']=workshop_participants.shape[0]
        quiz_plot_df['Not attempted'] = quiz_plot_df['Not attempted']-quiz_plot_df.Correct-quiz_plot_df.InCorrect
        quiz_plot_df = quiz_plot_df.sort_values(by='question').reset_index().drop('index', axis=1,errors='ignore')
               
        true_trace = go.Bar(x=quiz_plot_df['Correct'], y=quiz_plot_df['question'], orientation='h', name='True', text=quiz_plot_df['Correct'], 
                            textposition='inside', marker=dict(color='#748d94'), showlegend=False)
        false_trace = go.Bar(x=quiz_plot_df['InCorrect']*-1, y=quiz_plot_df['question'], orientation='h', name='False', text=quiz_plot_df['InCorrect'], 
                             textposition='inside', marker=dict(color='#9ac7d4'), showlegend=False)

        correct_colors = ['#879474' if ans else '#947474' for ans in quiz_plot_df['correct_answer']]

        correct_answers_trace = go.Bar(x=[1 if ans else 1 for ans in quiz_plot_df['correct_answer']], y=quiz_plot_df['question'], 
                                       orientation='h', name='Correct Answers', 
                                       text=['True' if ans else 'False' for ans in quiz_plot_df['correct_answer']], 
                                       textposition='inside', marker=dict(color=correct_colors), showlegend=False)

        fig = make_subplots(rows=1, cols=2, subplot_titles=('Participant Responses', 'Correct Answers'), column_widths=[0.9, 0.1])

        fig.add_trace(true_trace, row=1, col=1)
        fig.add_trace(false_trace, row=1, col=1)
        fig.add_trace(correct_answers_trace, row=1, col=2)

        fig.update_layout(go.Layout(barmode='relative', yaxis=dict(title='Questions')))

        fig.update_xaxes(title_text='Number of Responses', tickvals=[-quiz_plot_df.InCorrect.max()/2, 0.3 if quiz_plot_df.Correct.max()==0 else quiz_plot_df.Correct.max()/2], ticktext=['Incorrect', 'Correct'],range=[-len(workshop_participants.workshop_email.unique()), len(workshop_participants.workshop_email.unique())], row=1, col=1)
        fig.update_xaxes(showticklabels=False, row=1, col=2)
        fig.update_traces(textfont_size=16, textangle=0, textposition="inside", cliponaxis=False, textfont_color="black")
        fig.update_layout(autosize=False,height=300,margin=dict(l=1, r=30, t=20, b=0), font=dict(size=16, color='black',family="Nunito"))
        fig.update_xaxes(showline=False,linewidth=2,linecolor='#63316F',mirror=True,
                         tickfont=dict(size=16, color='black',family="Nunito"), title=dict(font=dict(size=16, color='black',family="Nunito")))
        fig.update_yaxes(showline=False,linewidth=2,linecolor='#63316F',mirror=True, tickangle = -90, 
                         tickfont=dict(size=16, color='black',family="Nunito"), title=dict(font=dict(size=16, color='black',family="Nunito")))

        st.plotly_chart(fig, theme="streamlit", use_container_width=True, config={'displayModeBar': False})      

    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown(f"<h5 style='text-align: left; color: {primary_font_color}; font-family: Nunito;'>Leaderboards for top 10 users</h5>", unsafe_allow_html=True)
    
    with st.expander(""):
        col1, col2, col3= st.columns(3)    
        cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ['#9ac7d4', '#90b8c4', '#87aab4', '#7d9ba4', '#748d94', '#6b7f85', '#617075', '#586265', '#4e5355', '#454545'])      
        col1.markdown(f"<h5 style='text-align: center; color: {primary_font_color}; font-family: Nunito;'>For past 90 days</h5>", unsafe_allow_html=True)
        with col1:
            components.html(
    css_start+workshop_emails[['name', 'past_MQI']].round(2).sort_values(by='past_MQI', ascending=True).rename(columns={'name':'Name', 'past_MQI':'MQI'})[:10].fillna(0).style.set_properties(subset=['MQI'], **{'text-align': 'center'}).background_gradient(cmap=cmap, axis=0).format({'MQI':'{:.0f}'}).hide(axis="index").to_html().replace(' border="1" class="dataframe"','').replace(' style="text-align: right;"','')+css_end,height=css_table_height)  
        
        col2.markdown(f"<h5 style='text-align: center; color: {primary_font_color}; font-family: Nunito;'>For 180 days</h5>", unsafe_allow_html=True)
        with col2:
            components.html(
    css_start+workshop_emails[['name', 'future_MQI']].round(2).sort_values(by='future_MQI', ascending=True).rename(columns={'name':'Name', 'future_MQI':'MQI'})[:10].fillna(0).replace(None,).style.set_properties(subset=['MQI'], **{'text-align': 'center'}).background_gradient(cmap=cmap, axis=0).format({'MQI':'{:.0f}'}).hide(axis="index").to_html().replace(' border="1" class="dataframe"','').replace(' style="text-align: right;"','')+css_end,height=css_table_height)      
        
        col3.markdown(f"<h5 style='text-align: center; color: {primary_font_color}; font-family: Nunito;'>For 2030</h5>", unsafe_allow_html=True)
        with col3:
            components.html(
    css_start+workshop_emails[['name', 'for_2030']].round(2).sort_values(by='for_2030', ascending=True).rename(columns={'name':'Name', 'for_2030':'MQI'})[:10].fillna(0).style.set_properties(subset=['MQI'], **{'text-align': 'center'}).background_gradient(cmap=cmap, axis=0).format({'MQI':'{:.0f}'}).hide(axis="index").to_html().replace(' border="1" class="dataframe"','').replace(' style="text-align: right;"','')+css_end,height=css_table_height)


global primary_font_color
primary_font_color ='#858585'
dialog_container = float_dialog(
    not ss.is_login  # If login is false dialog will be displayed.
    # ,css='padding-top: 5px;'  # Beautify the float diablog box.
)

# Shows the dialog container.
with dialog_container:
    def update_login_status():
        """A callback from OK button on this dialog box."""
        if ss.password == 'mynzo2023':
            ss.is_login = True
        else:
            ss.err_msg = 'Incorrect username/password'

    st.markdown("## :blue[Login]")
    st.markdown("<style>h2 {padding: 0;}</style>", unsafe_allow_html=True)

    st.text_input('Password', type='password', key='password')
    st.button("OK", on_click=update_login_status)
    msg = st.empty()

if ss.err_msg:
    msg.error(ss.err_msg)

if ss.is_login:
    seques_plan_new = pd.DataFrame()
    # st.sidebar.markdown(f"<h5 style='text-align: left; color: {primary_font_color}; font-family: Nunito;'>Enter Dashboard password</h5>", unsafe_allow_html=True)
    # password = st.sidebar.text_input('enter pass', label_visibility = 'collapsed', type="password")
    # if password == 'mynzo2023':
    try:
        mynzo_db_read = pymysql.connect(host=sql_hostname, user=sql_username,
                               passwd=sql_password, db=sql_main_database)
        live_workshops = pd.read_sql_query('''select id, name from workshop where is_live=1;''', mynzo_db_read)

        mynzo_db_read.close()

        if live_workshops.shape[0]>0:
            st.sidebar.markdown(f"<h5 style='text-align: left; color: {primary_font_color}; font-family: Nunito;'>Choose Workshop</h5>", unsafe_allow_html=True)
            global workshop_choice
            workshop_choice = st.sidebar.radio('select Workshop', [x for x in live_workshops.name], label_visibility ='collapsed' ) 
            global choice
            choice = live_workshops[live_workshops.name == workshop_choice].id.item()
            all_quizzes = quiz_list(quiz_list_url, choice)

            st.sidebar.markdown(f"<h5 style='text-align: left; color: {primary_font_color}; font-family: Nunito;'>Choose Currency</h5>", unsafe_allow_html=True)
            global currency_choice
            currency_choice = st.sidebar.radio('Choose Currency', ['USD ($)', 'INR (₹)'], label_visibility ='collapsed' )

            st.sidebar.markdown(f"<p style='text-align: center; padding-top:-5px; color: {primary_font_color}; font-family: Nunito;'><ins><i>App will show all analytics related to Mynzo Workshop {live_workshops[live_workshops.id == choice].name.item()}</i></ins></p>", unsafe_allow_html=True)
            workshop_analytics(all_quizzes)

            if 'date_key' not in st.session_state:
                st.session_state['date_key'] = pd.Timestamp.utcnow()

            st.session_state['date_key'] = pd.Timestamp.utcnow()
            sidebar_comp = st.sidebar
            with sidebar_comp:
                st.components.v1.html(html_time_reset.replace('last_reload_time', str(st.session_state['date_key'].timestamp() * 1000)).replace('current_time',"new Date().getTime()"), height=50)

        else:
            st.sidebar.markdown(f"<h7 style='text-align: left; color: {primary_font_color}; font-family: Nunito;'>No live workshop available currently</h7>", unsafe_allow_html=True)
    except:
        st.sidebar.markdown(f"<h3 style='text-align: left; color: {primary_font_color}; font-family: Nunito;'>🙂 Please refresh the Page</h3>", unsafe_allow_html=True)
                
