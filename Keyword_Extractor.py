from bs4 import BeautifulSoup
import requests
from nltk.corpus import stopwords
import re

class Keywords:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        pass
    
    def content_from_url(self, url= 'https://pib.gov.in/Allrel.aspx'):
        
        response = requests.get(url)
        
        if response.status_code == 200:
            s = set()
            content = response.text
            soup = BeautifulSoup(content, 'html5lib')
            content = soup.find_all('ul', {'class': 'num'})
            for keywords in content:
                keywords = keywords.get_text()
                keywords = re.sub('[!:,.!@#$%()]', '', keywords)
                keywords = keywords.split()
                for keyword in keywords:
                    keyword = keyword if keyword not in self.stop_words and not keyword.isdigit() else None
                    if keyword:
                        keyword = keyword.lower()
                        s.add(keyword)
            return s
        
        return None
            
            

ke = Keywords()

ke.content_from_url()