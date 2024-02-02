# Venture.py
import requests
import pandas as pd
import numpy as np
# pd.set_option('display.max_rows', None)
import re
from datetime import date
import os
import sys
import urllib.request
import json
import time

class Venture():
    """
    Using examples:
        venture = Venture()
        df = venture.get_all_venture_names()
        df = venture.preprocessing_ventures(df)
        df = venture.check_validate_date(df)
    """


    def __init__(self):
        # 221230 기준 최신화
        self.model = "​/15084581​/v1​/uddi:80541c9b-7fb6-4bf8-9e60-97bd26ac94c1"

    def get_all_venture_names(self):
        """
        External Libraries : pandas, requests 

        GET all venture names from DATA.GO.KR (open source)
        """

        def get_1000_venture_names(pages):
            """
            model changes every month
            """
            response = requests.get(
                 f"https://api.odcloud.kr/api/15084581/v1/uddi:80541c9b-7fb6-4bf8-9e60-97bd26ac94c1?page={pages}&perPage=1000&serviceKey=pkPwO0GEOz6XS1KY122J7qMsJO2oahKvFAcO5yBf%2Bg7Xq1Sy8npChjS9utX%2FPn4pLnhDCQQMoGvLb4izT7CBLA%3D%3D"
            )
            if response.status_code == 200:
                companies = response.json()
                return companies['data']
            else:
                print("Error: Unable to get data. Check the API once more.")
            
        pages = 1
        ventures = []
        while True:
            new_ventures = get_1000_venture_names(pages)
            if not new_ventures:
                break
            ventures += new_ventures
            pages += 1

        # print(len(ventures))
        return pd.DataFrame(ventures)


    def preprocessing_ventures(self, df):
        """
        venture 기업들에 대한 정보들 전처리
        """
        
        # drop unnecessary columns
        unnecessaries = ['대표자명', '벤처확인기관', '벤처확인유형', '주소(현재본사주소)', '지역(벤처확인신청당시)']
        for unnecessary in unnecessaries:
            try:
                df.drop(columns=unnecessary, inplace=True)        
            except:
                pass
        
        def preprocess_jobcategories(str_content):
            str_content = re.sub('및', '', str_content)
            str_content = re.sub('기타', '', str_content)
            str_content = re.sub('그', '', str_content)
            str_content = re.sub('외', '', str_content)
            str_content = re.sub('업', '', str_content)
            str_content = re.sub(' +', ' ', str_content)
            return str_content.strip()

        df['업종명'] = df['업종명'].apply(preprocess_jobcategories)

        print(f"{df.업종명.nunique()}개의 업종명이 존재합니다.")

        return df

    def check_validate_date(self, df):
        """
        check whether 유효시작일 < 현재 < 유효종료일
        """
        # str type
        now = date.today().strftime('%Y-%m-%d')
        
        def is_over(end_date):
            
            return str(end_date) < now

        def is_not_yet(start_date):
            
            return now < str(start_date)

        df['is_over'] = df['유효종료일'].apply(is_over)
        df['is_not_yet'] = df['유효시작일'].apply(is_not_yet)

        df = df[df['is_over']==False]
        df = df[df['is_not_yet']==False]

        df.drop(columns = ['유효시작일', '유효종료일', 'is_over', 'is_not_yet'], inplace = True)

        df.columns = ['industry_name', 'industry_classification', 'company_name', 'serial_number', 'main_product']
        
        return df

    def job_translation(self, df):
        """
        df : venture information dataframe
        """
        # detect whether it is possible to run free Papago NMT API
        jobs = df['industry_name'].drop_duplicates()
        
        papago_possible = False
        # check
        total_length = ""
        for job in jobs:
            total_length += job
        print(len(total_length))
        if len(total_length) <= 10000:
            papago_possible = True
        
        def run_papago(jobs):

            # return ["Business", "Science"] # for test

            client_id = "API_ID" # 개발자센터에서 발급받은 Client ID 값
            client_secret = "API_SECRET" # 개발자센터에서 발급받은 Client Secret 값

            jobs_eng = []

            for job in jobs:

                # 단어 하나만 번역이 가능
                encText = urllib.parse.quote(job)
                data = "source=ko&target=en&text=" + encText
                url = "https://openapi.naver.com/v1/papago/n2mt"
                request = urllib.request.Request(url)
                request.add_header("X-Naver-Client-Id",client_id)
                request.add_header("X-Naver-Client-Secret",client_secret)
                response = urllib.request.urlopen(request, data=data.encode("utf-8"))
                rescode = response.getcode()
                if(rescode==200):
                    response_body = response.read()
                    try:
                        result = response_body.decode('utf-8')
                        result = json.loads(result) # dict
                        result = result['message']['result']['translatedText']
                        
                        jobs_eng.append(result)
                        time.sleep(0.1)

                    except:
                        print("error in printing result")
                else:
                    print("Error Code:" + rescode)

            return jobs_eng

        if papago_possible:
            return run_papago(jobs)
        else:
            print("text number overload. please make it under 10,000.")
