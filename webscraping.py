from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
from time import time
from sentiment import sentiment
import json
import joblib 
from nltk.corpus import stopwords

class Scraping:
    def __init__(self, language= 'english', count = 10):
        self.count = count
        self.language = language.lower()
        self.text_file = "Scraping sites/" + self.language + ".txt"
        self.jsons = []
        self.stopwords = stopwords.words('english')
        
        self.main_language = 'english'
    
    def json_for_kv_and_text(self, k_v, text, url, article_name):
        jsonContent = {}
        jsonContent['id'] = len(self.jsons)
        jsonContent['content'] = text
        jsonContent['tonality'] = k_v[next(iter(k_v))][0]['label']
        jsonContent['time'] = time()
        jsonContent['article'] = article_name.lstrip()[:60]+ '...'
        jsonContent['url'] = url
        keywords_file = joblib.load('Keywords/keywords')
        import random
        keywords = set()
        for _ in range(5):
            word = random.choice(list(keywords_file))
            if word in self.stopwords:
                word = random.choice(list(keywords_file))
            keywords.add(word)
        jsonContent['keywords'] = list(keywords)
        
        return jsonContent
        
        
    
    def _get_data_about_topic(self, url, content_selector, article_name):
        text = ''
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html5lib')
            government_texts = soup.select(content_selector)
            for data in government_texts:
                text += data.get_text()
                break
        k_v_pairs = self.get_sentiment_scores(text)
        
        jsonContent = self.json_for_kv_and_text(k_v_pairs, text, url, article_name)
        self.jsons.append(jsonContent)
        
        # with open('demo.txt', 'w') as f:
        #     f.write(text)
        #     f.write(f"\n\n\nScores: {k_v_pairs}\n\n\n\n")
        
        
        return text
            
    def get_sentiment_scores(self, text):
        keywords_file = joblib.load('Keywords/keywords')
        import random
        keywords = set()
        for _ in range(5):
            keywords.add(random.choice(list(keywords_file)))
        k_v_pairs = sentiment(text, keywords)
        
        return k_v_pairs
        
        
    
    def _get_heading_from_url(self, url, href_id, content_selector):
        text = ''
        response = requests.get(url)
        
        if response.status_code == 200:
            
            soup = BeautifulSoup(response.text, 'html5lib')
            government_hrefs = soup.find_all('a', {'class': href_id})
            count = 0
            data_urls = set()
            for hrefs in tqdm(government_hrefs, total= self.count):
                article_name = hrefs.get_text()
                data_url = hrefs['href']
                if data_url in data_urls:
                    continue
                
                data_urls.add(data_url)
                count += 1
                text += self._get_data_about_topic(data_url, content_selector, article_name)
                if count == self.count:
                    break
            return text

        return f"{url} failed to fetch data"
        
    
    def _translate_from_regional_to_english(self, text):
        
        if self.language == self.main_language:
            return text

        from googletrans import Translator
        translator = Translator()
        translated_text = translator.translate(text, src = 'hi', dest= 'en')
        
        return translated_text
        
            
    def get_site_name_from_txt(self):
        
        with open(self.text_file, 'r') as f:
            url, href_id, content_selector = f.readline().split(',')
            
            content = self._get_heading_from_url(url, href_id, content_selector)
            
            if not (self.language == self.main_language):
                content = self._translate_from_regional_to_english(content)
    
    
        
        
   
scraper = Scraping("english")

start = time()
scraper.get_site_name_from_txt()
end = time()

with open('scraped/webscraping.json', 'a') as f:
            json.dump(scraper.jsons, f)

print(f"Time taken: {end-start}")