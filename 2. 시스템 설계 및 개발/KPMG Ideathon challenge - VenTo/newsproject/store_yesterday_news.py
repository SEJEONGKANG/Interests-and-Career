import sqlite3
# import functools
from datetime import date, timedelta
import time
import pandas as pd
from ventures import Venture
from get_news import get_yesterday_metadata, get_bbc_content
from create_news_db import News4service3, get_jobs_eng
import schedule

def venture_job():
    try:
        # make connection to the vento.db
        con = sqlite3.connect("../ventoproject/vento.db")
        venture = Venture()
        jobs_kor = venture.get_all_venture_names()
        jobs_kor = venture.preprocessing_ventures(jobs_kor)
        jobs_kor = venture.check_validate_date(jobs_kor)
        # jobs_kor.to_csv('/s1_ventures_kor.csv', index=False, encoding='utf-8')
        jobs_kor.to_sql('s1_ventures_kor', con)
        
        jobs_eng = venture.job_translation(jobs_kor)
        jobs_kor.to_sql('s1_ventures_kor', con)
        jobs_eng.to_sql('s1_ventures_eng', con)

        con.commit()
        
    except:
        print("error occured.")
    finally:
        # close the DB connection
        con.close()

def news_job():
    try:
        # connect : sqlite db를 생성 혹은 접근
        conn = sqlite3.connect("/Users/junwooahn/flask_dev/ventoproject/vento.db")

        # # #Creating a cursor object using the cursor() method
        cursor = conn.cursor()
        
        try:
            cursor.execute("DROP TABLE news4company")
            print("yesterday_news table dropped... initializing DB...")
        except:
            pass
        
        # pandas data to sqlite db
        # get metadata
        
        yesterday = date.today() - timedelta(1)
        yesterday = yesterday.strftime('%Y-%m-%d')
        print(yesterday)
        
        metadata_df = get_yesterday_metadata(api_key="NEWS_API_api_key_for_developers_plan", source='bbc-news', date=yesterday)

        print(metadata_df)
        
        bbc_content_df = get_bbc_content(metadata_df)
        
        bbc_content_df = pd.read_sql("SELECT * FROM news", conn, index_col=None)
        ventures_kor = pd.read_sql("SELECT * FROM s3_ventures_kor", conn, index_col=None)
        ventures_eng = pd.read_sql("SELECT * FROM s3_ventures_eng", conn, index_col=None)
        print(bbc_content_df)
        print(ventures_kor)
        print(ventures_eng)
        
        bbc_content_df = bbc_content_df.iloc[:50, :]
        
        # return 
        jobs_eng = get_jobs_eng(ventures_eng)
        
        #1. Initialize
        service3 = News4service3(bbc_content_df, ventures_kor, ventures_eng, jobs_eng)
        
        del bbc_content_df
        del ventures_kor
        del ventures_eng

        #2. evaluate cosine_similarity
        similarity_df = service3.get_cosine_similarity_df()

        print("similarity finished")

        #3. get news with top10 cosine similarity 업종명
        filtered_news = service3.cosine_sim_topN(similarity_df)
        
        print("topN finished")
        
        #4. filter top3 업종명 using zero-shot classification
        filtered_news = service3.get_top3_domains()

        print("3 top finished")

        #5. clustering 진행
        _, cluster_labels = service3.get_job_cluster(k=40)

        print("got cluster_labels")
        
        #6. 업종에 대해 어느 클러스터인지 mapping한 DataFrame 생성
        cluster_res = service3.get_industry_cluster_map(cluster_labels)
        del cluster_labels

        print("got cluster result")

        #7. get tables to be stored in a DB
        filtered_news = service3.get_news_by_cluster(cluster_res)

        print("got fnal news")
        print(filtered_news.head())
        
        auth_table = service3.get_auth_table(cluster_res)

        print("got fnal auth")
        del cluster_res
        print(auth_table.head())
        
        filtered_news = filtered_news.drop(columns=['topN'])
        print(list(filtered_news.columns))
        
        try:
            cursor.execute("DROP TABLE news")
            print("news table dropped... initializing DB...")
        except:
            print('saving filtered news to news TABLE...')
        
        filtered_news.to_sql('s3_news', conn)
        print("saving as ")
        
        auth_table.to_sql('s3_auth', conn)
        
        
        # #Commit your changes in the database
        conn.commit()
        print("DB changes commit")

    except:
        print("Error occured. Please check encodings")

    finally:
        # Closing the connection
        conn.close()
        print("DB connection closing ...")

if __name__ == "__main__":
    
    # with no scheduling : for test
    # news_job()
    
    news_scheduler = schedule.Scheduler()
    ventures_scheduler = schedule.Scheduler()
    
    news_scheduler.every().day.at("09:01").do(news_job)
    # # check whether API has changed
    ventures_scheduler.every().day.at("00:01").do(venture_job)
    
    # i = 0
    while True:
        schedule.run_pending()
        
        time.sleep(1)
        i += 1
        if i % 10 == 0:
            print(f"{i}초 경과")