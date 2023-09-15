from bs4 import BeautifulSoup
import requests
from pprint import pprint
class Scraping:
    def __init__(self, language= 'english'):
        self.language = language.lower()
        self.text_file = self.language + ".txt"
        
        self.main_language = 'english'
    
    def _get_data_about_topic(self, url):
        text = ''
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html5lib')
            government_texts = soup.find_all('p')
            for data in government_texts:
                text += data.get_text()
                
        return text
            
    
    def _get_heading_from_url(self, url):
        text = ''
        response = requests.get(url)
        
        if response.status_code == 200:
            
            soup = BeautifulSoup(response.text, 'html5lib')
            government_hrefs = soup.find('div', {'class': 'bolly-news-listing'})
            
            government_hrefs = government_hrefs.find_all('a')
            for hrefs in government_hrefs:
                print(hrefs)
                data_url = hrefs['href']
                text += self.get_data_about_topic(data_url)
            
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
            url = f.readline()
            content = self.get_heading_from_url(url)
            
            if not (self.language == self.main_language):
                content = self._translate_from_regional_to_english(content)
                       
            print(content.text)
    
    
        
        
        
        
scraper = Scraping("english")

scraper.get_site_name_from_txt()