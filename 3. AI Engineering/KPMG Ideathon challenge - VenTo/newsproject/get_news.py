import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from transformers import pipeline
    
# pd.set_option('display.max_rows', None)

# return articles as dataframe
def get_yesterday_metadata(api_key, source, date):
    """
    get metadata of BBC news of 'tech' and 'science' cateogry using News API
    
    api_key : api_key for NEWS API, developer's license
    source  : news website to get articles, BBC has confirmed us for using in KPMG 2023 Ideathon
    
    returns a dataframe of 
        source, author, title, description, url, urlToImage, publishedAt(time), content(only small part of total text)
    of yesterday BBC news articles
    """
    api_key = api_key
    source = source
    
    # print(date, "this is test")
    
    def get_articles(page, date):
        response = requests.get(
            f"https://newsapi.org/v2/everything?sources={source}&from={date}&to={date}&page={page}&apiKey={api_key}"
        )
        if response.status_code == 200:
            articles = response.json()
            return articles['articles']
        else:
            print("Error: Unable to fetch articles")
            return []
    # Keep track of the current page number
    page = 1

    # Initialize a list to store the articles
    articles = []

    # Fetch articles until API request limit is reached or there are no more articles
    while True:
        #time.sleep(3)
        new_articles = get_articles(page, date)
        print(f"{page} 진행중")
        if not new_articles:
            break
        articles += new_articles
        page += 1
    
    return pd.DataFrame(articles)

def get_bbc_content(df):
    """
    df : get the result of get_yesterday_metadata()
    
    get the text content of BBC news by using News API metadata
    """
    
    def get_bbc_text(url):
        response = requests.get(url, verify=False)
        html_content = response.content

        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # sport has a dirrent web architecture
        if 'sport' in url:
            try:
                # Find the main content of the article
                main_content = soup.find('div', {'class': 'qa-story-body story-body gel-pica gel-10/12@m gel-7/8@l gs-u-ml0@l gs-u-pb++'})

                # Extract the text of the article
                article_text = main_content.get_text()

                # Print the extracted text
                return article_text

            except:
                pass

        else:  
            # Find the article text by searching for the correct HTML tags
            article_text = ""
            for p in soup.find_all("div", class_="ssrcss-11r1m41-RichTextComponentWrapper ep2nwvo0"):
                article_text += p.get_text()

            return article_text
    
    def drop_rows(text):
        if text == None:
            return False
        elif len(text) < 10:
            return False
        return True
    
    df.loc[:,'original_text'] = df.loc[:,'url'].apply(get_bbc_text)
    
    # df.loc['original_text'] = org_txt
    rows = df.loc[:, 'original_text'].apply(drop_rows)
    df =  df.loc[rows,:]
    
    df.loc[:, 'source'] = df.loc[:, 'source'].apply(lambda x: dict(x)['name'])
    print('done...')
    
    df = df.drop(columns=['author', 'description', 'content'])
    
    return pd.DataFrame(df)
