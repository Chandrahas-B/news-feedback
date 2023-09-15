from bs4 import BeautifulSoup
import requests
from time import time


class Scraping:
    def __init__(self, language= 'english'):
        self.language = language.lower()
        self.text_file = self.language + ".txt"
        
        self.main_language = 'english'
    
    def _get_data_about_topic(self, url, content_id):
        text = ''
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html5lib')
            government_related_tag = soup.find('div', {'class': content_id})
            if government_related_tag is None:
                return ''
            print(government_related_tag)
            government_texts = government_related_tag.find_all('p')
            for data in government_texts:
                text += data.get_text()
                
        return text
            
    
    def _get_heading_from_url(self, url, href_id, content_id):
        text = ''
        response = requests.get(url)
        
        if response.status_code == 200:
            
            soup = BeautifulSoup(response.text, 'html5lib')
            government_hrefs = soup.find_all('a', {'class': href_id})
            
            for hrefs in government_hrefs:
                data_url = hrefs['href']
                text += self._get_data_about_topic(data_url, content_id)
            
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
            url, href_id, content_id = f.readline().split(',')
            content = self._get_heading_from_url(url, href_id, content_id)
            
            if not (self.language == self.main_language):
                content = self._translate_from_regional_to_english(content)
                       
            print(content.text)
    
    
        
        
        
start = time()    
scraper = Scraping("english")

scraper.get_site_name_from_txt()
end = time()

print(f"Time taken: {start-end}")