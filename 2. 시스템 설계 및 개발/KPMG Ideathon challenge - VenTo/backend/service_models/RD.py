import pandas as pd
from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util
import torch

class RD():

  def __init__(self, data, text, heading, embedded):
    self.data = data
    self.text = text
    self.heading = heading
    self.okt = Okt()
    self.embedded = embedded
  
  def similarity(self, data, text, heading, okt, embedded):

    data = data[data['main_topic']==heading].reset_index()

    def keyword_extractor_target(self, okt, text):
      tokens = okt.phrases(text)
      tokens = [ token for token in tokens if len(token) > 1 ] # 한 글자인 단어는 제외
      count_dict = [(token, text.count(token)) for token in tokens ]
      ranked_words = sorted(count_dict, key=lambda x:x[1], reverse=True)[:10]
      lst = [ keyword for keyword, freq in ranked_words ]
      text = ''
      for i in lst:
        text = text + ' ' + i
      return text

    # 유사도 계산식
    def similarity_calc (self, data, target, embedded_one):
      model = SentenceTransformer('jhgan/ko-sroberta-sts')
      embedding_dfs = embedded_one
      
      embedding_item = model.encode(target,convert_to_tensor=True)
      temp = util.pytorch_cos_sim(embedding_dfs, embedding_item)
      temp = pd.DataFrame(temp, columns = ['코사인']).astype('float')
      data = pd.concat([data, temp], axis=1)
      return data
      
    # 과제별 유사도 계산(ox)
    def simil_test(self, keyword, text):
      sim_score = 0
      for j in keyword:
        if j in text:
          sim_score += 1
          break
        else:
          continue
      return sim_score

    data['유사도1'] = data['keyword'].apply(lambda x: simil_test(self, x, text))
    data = similarity_calc(self, data, text, embedded)
    data = data[data['유사도1']==1]

    data = data.sort_values('코사인', ascending=False).reset_index()
    
    return data

  def recommend(self):
    lst = self.similarity(self.data, self.text, self.heading, self.okt, self.embedded)
    lst = lst[['announcement_name']][:5]
    return lst

  def similar(self):
    lst = self.similarity(self.data, self.text, self.heading, self.okt, self.embedded)
    lst = lst[['support_name']][:10]
    return lst

