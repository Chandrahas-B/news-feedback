from bs4 import BeautifulSoup
import requests
from nltk.corpus import stopwords
import re
import joblib
import insert_headings_mongo

class Keywords:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        pass
    
    def content_from_url(self, url= 'https://pib.gov.in/Allrel.aspx'):
        
        response = requests.get(url)
        
        if response.status_code == 200:
            content = response.text
            soup = BeautifulSoup(content, 'html5lib')
            pib_topic_releases = soup.find_all('ul', {'class': 'num'})
            
            for pib_release in pib_topic_releases:
                releases = pib_release.find_all('li')
                for release in releases:
                    news_heading = release.get_text()
                    insertion = insert_headings_mongo.insert_document_to_collection(news_heading)
                    print(insertion)               
            
        
        return None
            
            

ke = Keywords()

keywords = ke.content_from_url()

joblib.dump(keywords, 'keywords')