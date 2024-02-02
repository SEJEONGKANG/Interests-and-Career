import sqlite3
import re
import pandas as pd
import numpy as np
import torch
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine
# from IPython.display import display
from transformers import pipeline
from transformers import DebertaTokenizer, DebertaModel
from sklearn.cluster import KMeans

'''
Works in Google Colab Pro, cuda

# # Dataset
# news = pd.read_csv('/content/drive/MyDrive/KPMG/news.csv') # renewed every day

# ventures_kor = pd.read_excel('/content/drive/MyDrive/KPMG/pipeline/ventures.xlsx') # renewed when data.go.kr updates 중소벤처기업명단 API

# news = news.head()

# # we've tested 'googletrans', 'papago free API', and 'google document translation by manual'. The latter showed best performance
# ventures_eng = pd.read_excel('/content/drive/MyDrive/KPMG/pipeline/ventures_eng.xlsx') # translated version of ventures_kor by "google document translation"

'''
def get_jobs_eng(ventures_eng):
    ventures_eng.loc[:,'industry_name'] = ventures_eng.loc[:,'industry_name'].apply(lambda x: x.lower())

    # set stop_words
    stop_words = ['manufacturing of', 'manufacture of', 'unclassified']
    for i in range(len(stop_words)):
        ventures_eng.loc[:,'industry_name'] = ventures_eng.loc[:,'industry_name'].str.replace(stop_words[i], '')

    ventures_eng.loc[:,'industry_name'] = ventures_eng.loc[:,'industry_name'].apply(lambda x: x.strip())

    jobs_eng = ventures_eng.loc[:,'industry_name']
    jobs_eng = jobs_eng.drop_duplicates()
    jobs_eng = jobs_eng.reset_index(drop=True)
    print(f"{len(jobs_eng)}개의 고유한 업종명이 존재합니다.")
    return jobs_eng

class News4service3():

    def __init__(self, news, ventures_kor, ventures_eng, jobs_eng):
        
        self.news = news
        self.ventures_kor = ventures_kor
        self.ventures_eng = ventures_eng
        self.jobs_eng = jobs_eng
    
    # News filtering part

    def get_cosine_similarity_df(self, MODEL_NAME='sentence-transformers/all-MiniLM-L6-v2', MAX_SEQ_LENGTH=512):
        """
        Embeding with sentence BERT
        MODEL_NAME = 'sentence-transformers/all-MiniLM-L6-v2'
        MAX_SEQ_LENGTH = 512
        """

        model = SentenceTransformer(MODEL_NAME)
        model.max_seq_length = MAX_SEQ_LENGTH

        
        if torch.cuda.is_available():
            device = torch.device("cuda")
            model.to(device)
        else:
            device = torch.device("cpu")

        news_texts_embeddings = model.encode(self.news.loc[:, 'original_text'], convert_to_tensor=True, device=device).cpu().detach().numpy()

        short_words_embeddings = model.encode(self.jobs_eng.reset_index(drop=True), convert_to_tensor=True, device=device).cpu().detach().numpy()

        # pd.set_option('display.max_columns' , None)
        return pd.DataFrame([[1 - cosine(news_texts_embeddings[i], short_words_embeddings[j]) for j in range(len(self.jobs_eng))] for i in range(len(self.news))], columns = self.jobs_eng)

    def cosine_sim_topN(self, similarity_df, N=10):
        """
        기사 기준으로 cosine similarity가 높은
        상위 N개의 업종명을 저장하기 위한 함수
        """
        self.news.loc[:,'topN'] = similarity_df.apply(lambda x: list(x.nlargest(N).index), axis=1)
        return self.news

    def get_top3_domains(self):
        """
        input : news with cosine_similarity
        output : news with top3 domain labels
        """
        def multi_category_score(text, label):

            device = 0 if torch.cuda.is_available() else -1            

            classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device = device)
            candidate_labels = label

            result = classifier(text, candidate_labels, multi_label=True)

            return result['labels'][:3]

        # Making Inference
        self.news[['first_label', 'second_label', 'third_label']] = self.news.apply(lambda row: multi_category_score(row['original_text'], row['topN']), axis=1, result_type='expand')
        
        # drop original_text : 저작권 이슈
        self.news = self.news.drop(columns=['original_text'])
        return pd.DataFrame(self.news)

    #  Clustering Part

    def get_job_cluster(self, k=40):
        """
        return : (kmeans_model, cluster_labels)
        """
        word_list = list(self.jobs_eng)

        tokenizer = DebertaTokenizer.from_pretrained('microsoft/deberta-base')
        # model = DebertaModel.from_pretrained('microsoft/deberta-base').to('cuda')
        model = DebertaModel.from_pretrained('microsoft/deberta-base')

        word_vectors = []
        for word in word_list:
            # input_ids = torch.tensor(tokenizer.encode(word, add_special_tokens=True)).unsqueeze(0).to('cuda')
            input_ids = torch.tensor(tokenizer.encode(word, add_special_tokens=True)).unsqueeze(0)
            with torch.no_grad():
                embeddings = model(input_ids)[0].squeeze(0).mean(0)
            word_vectors.append(embeddings.cpu().numpy())

        n_clusters = k
        kmeans = KMeans(n_clusters=n_clusters, random_state=42).fit(word_vectors)
        cluster_labels = kmeans.labels_

        return kmeans, cluster_labels


    def get_industry_cluster_map(self, cluster_labels):
        """
        use after
        _, cluster_labels = service3.get_job_cluster(k=40)
        """
        cluster_res = pd.DataFrame([self.jobs_eng, cluster_labels]).transpose()
        cluster_res.columns = ['industry_name', 'cluster_number']
        # cluster_res.to_csv('/content/drive/MyDrive/KPMG/pipeline/cluster_map.csv',index=False)
        cluster_res = cluster_res.reset_index(drop=True)
        # cluster_res.to_csv('/content/drive/MyDrive/KPMG/pipeline/clustering_result.csv',index=False)
        return cluster_res
    
    # Combine filtered news with cluster : cluster makes robust recommand even when there are changes in 업종명 in the future

    def get_news_by_cluster(self, cluster_res):
        """
        use after
        cluster_res = service3.get_industry_cluster_map(cluster_labels)
        returns the final form of news in DB
        """

        cluster_dict = dict(zip(cluster_res.loc[:,'industry_name'], cluster_res.loc[:,'cluster_number']))

        self.news.loc[:,'cluster1'] = self.news.loc[:,'first_label'].map(cluster_dict)
        self.news.loc[:,'cluster2'] = self.news.loc[:,'second_label'].map(cluster_dict)
        self.news.loc[:,'cluster3'] = self.news.loc[:,'third_label'].map(cluster_dict)
        
        return self.news

    # A function to identify who logged in

    def get_auth_table(self, cluster_res):
        """
        after getting cluster_res from the function : get_industry_cluster_map,

        creating auth_table used to track company cluster before filtering yesterday news
        """
        company_cluster = self.ventures_eng.merge(cluster_res, how="left", on="industry_name")

        print("company_cluster")
        print(company_cluster.head())
        
        def clean_jobs(text):
            text = re.sub(r"\((.*?)\)", "", text)
            return re.sub("㈜", "", text)

        
        auth_table = pd.concat([self.ventures_kor.loc[:,'company_name'], company_cluster.loc[:,'cluster_number']], axis = 1)
        
        print("auth_table")
        print(auth_table)
        
        
        auth_table.loc[:,'company_name'] = auth_table.loc[:,'company_name'].apply(clean_jobs)
        
        return auth_table
