from pydantic import BaseModel
from typing import List,Dict
from bs4 import BeautifulSoup
import re
from tqdm import tqdm
import requests
import time
import feedparser
from concurrent.futures import ThreadPoolExecutor, as_completed

feeds = [
    "https://www.dealnews.com/c142/Electronics/?rss=1",
        "https://www.dealnews.com/c39/Computers/?rss=1",
        "https://www.dealnews.com/c238/Automotive/?rss=1",
        "https://www.dealnews.com/f1912/Smart-Home/?rss=1",
        "https://www.dealnews.com/c196/Home-Garden/?rss=1",
       ]

def extract(html_snippet:str)->str:
    
    soup = BeautifulSoup(html_snippet,'html.parser')
    snippet_div = soup.find('div',class_='snippet summary')
    
    if snippet_div:
        description = snippet_div.get_text(strip=True)
        description = BeautifulSoup(description,'html.parser').get_text()
        description = re.sub('<[^<]+?>', '', description)
        result = description.strip()
    else:
        result = html_snippet
    return result.replace('\n',' ')

class ScrapedDeal:
    category: str
    title: str
    summary: str
    url: str
    details: str
    features: str
    
    def __init__(self,entry:Dict[str,str]):
        self.title = entry.get('title','')
        self.summary = entry.get('summary','')
        self.url = entry.get('link','')
        stuff = requests.get(self.url).content
        soup = BeautifulSoup(stuff,'html.parser')
        content = soup.find('div', class_='content-section').get_text()
        content  = content.replace('\nmore','').replace('\n',' ')
        if "Features:" in content:
            self.details, self.features = content.split("Features:")
        else:
            self.details = content
            self.features = ""
        
    def __repr__(self)->str:
        return f"<{self.title}>"
    
    def describe(self)->str:
        return f"Title: {self.title}\nDetails: {self.details.strip()}\nFeatures: {self.features.strip()}\nURL: {self.url}"
        

    @classmethod
    def fetch(cls, show_progress: bool = True, max_workers: int = 10):
        deals = []
        feed_iter = tqdm(feeds) if show_progress else feeds
        
        entries = []
        for feed_url in feed_iter:
            feed = feedparser.parse(feed_url)
            entries.extend(feed.entries[:10])
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_entry = {executor.submit(cls, entry): entry for entry in entries}
            
            for future in tqdm(as_completed(future_to_entry), total=len(future_to_entry)):
                try:
                    deal = future.result()
                    deals.append(deal)
                except Exception as e:
                    print(f"Error fetching deal: {e}")
        
        return deals
    
class Deal(BaseModel):
    product_description: str
    price: float
    url: str


class DealSelection(BaseModel):
    deals: List[Deal]
    
class Opportunity(BaseModel):
    deal: Deal
    estimate: float
    discount: float