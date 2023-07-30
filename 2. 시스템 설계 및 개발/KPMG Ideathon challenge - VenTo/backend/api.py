import time
from flask_cors import CORS
from flask import Flask, jsonify, make_response, request
import flask
from service_models.RD import RD
from service_models.Contract import Contract_Model, Contract_Model_Attention
import json
import pandas as pd
import sqlite3
import torch

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = sqlite3.connect('vento.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/rdtogether/reco', methods=['POST'])
def rdtogether_reco():

    item = request.form.get('item')
    category = request.form.get('industry')
    
    # Connect to vento.db
    conn = get_db_connection()
    
    result_dict = dict()
    
    # 새로나온 공고
    reco_data = pd.read_sql('SELECT * FROM additional_announcement',conn,index_col=None)
    
    reco = RD(data=reco_data,text=item,heading=category,embedded=torch.load('./torchs/reco'))
    reco = reco.recommend()
    find_reco = list(reco['announcement_name'])
    
    recoholders = ','.join('?' for _ in find_reco)
    
    reco_res = pd.read_sql(f'select dept_in_charge, announcement_name, date_of_deadline, dept_of_announcement, url, announcement_type, announced_amount, main_topic from additional_announcement where announcement_name in ({recoholders})', conn, params=find_reco, index_col=None)
    
    for i, item in reco_res.iterrows():
        result_dict[f"r{i}"] = list(item)
    
    result = json.dumps(result_dict, ensure_ascii=False)
    res = make_response(result)
    
    conn.close()
    
    return res

@app.route('/rdtogether/similar', methods=['POST'])
def rdtogether_similar():

    item = request.form.get('item')
    category = request.form.get('industry')
    
    # Connect to vento.db
    conn = get_db_connection()
    
    result_dict = dict()
    
    # 비슷한 공고
    similar_data = pd.read_sql('SELECT * FROM similarity',conn,index_col=None)
    
    similar_df = RD(data=similar_data,text=item,heading=category,embedded=torch.load('./torchs/similar'))
    similar_df = similar_df.similar()
    find_similar = list(similar_df['support_name']) 
    
    simholders = ','.join('?' for _ in find_similar)
    
    similar_res = pd.read_sql(f'select support_name from similarity where support_name in ({simholders})', conn, params=find_similar, index_col=None)
    
    for i, item in similar_res.iterrows():
        if i == 10:
            break
        result_dict[f"s{i}"] = list(item)
        
    result = json.dumps(result_dict, ensure_ascii=False)
    res = make_response(result)
    
    conn.close()
    
    return res

@app.route('/contracttogether', methods=['POST'])
def contract():
    file = request.files.get('file')
    threshold = request.form.get('sliderValue')
    threshold = round(float(threshold),2)
    contract = Contract_Model(file, threshold) #pdf, 기준치
    result = contract.create_lst()

    str_ = result[0][1]
    tmp = Contract_Model_Attention(str_)
    result_attention = tmp.create_lst()

    json_pre = {'sentences':result, 'attention':result_attention}
    json_done = json.dumps(json_pre, ensure_ascii=False)
    res = make_response(json_done)
    return res

@app.route('/issuetogether', methods=['POST'])
def issue():
    
    company_name = request.form.get('company_name')
    # print(company_name)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT cluster_number FROM auth WHERE company_name=?", (company_name,))
    cluster_num = cursor.fetchone()[0]
    
    reco_res = pd.read_sql(f'SELECT source, title, url, urlToImage from news4company where {cluster_num} = cluster1 or {cluster_num} = cluster2 or {cluster_num} = cluster3', conn, index_col=None)
    
    cols = list(reco_res.columns)
    
    result_dict = {}
    for i, content in reco_res.iterrows():
        result_dict[f'news{i}'] = dict()
        for j in range(len(list(content))):
            result_dict[f'news{i}'][cols[j]] = list(content)[j]
    
    
    result = json.dumps(result_dict, ensure_ascii=False)
    res = make_response(result)
    
    conn.close()
    
    return res
    