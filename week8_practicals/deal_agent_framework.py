import os
import sys
import logging
import json
from typing import List, Optional
from dotenv import load_dotenv
from pinecone import Pinecone
from agents.planning_agent import PlanningAgent
from agents.deals import Opportunity
from sklearn.manifold import TSNE
import numpy as np
import joblib



BG_BLUE = '\033[44m'
WHITE = '\033[37m'
RESET = '\033[0m'

CATEGORIES = ['Appliances', 'Automotive', 'Cell_Phones_and_Accessories', 'Electronics','Musical_Instruments', 'Office_Products', 'Tools_and_Home_Improvement', 'Toys_and_Games']
COLORS = ['red', 'blue', 'brown', 'orange', 'yellow', 'green' , 'purple', 'cyan']


def init_logging():
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "[%(asctime)s] [Agents] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S %z",
    )
    handler.setFormatter(formatter)
    
    file_handler = logging.FileHandler('pricer.log', mode="w") 
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    root.addHandler(file_handler)
    root.addHandler(handler)


class DealAgentFramework:
    
    index_name = 'products-vectorstore'
    MEMORY_FILE = 'memory.json'
    
    def __init__(self):
        init_logging()
        load_dotenv()
        self.vector_db = Pinecone(api_key=os.getenv('PINECONE_API_KEY')).Index(self.index_name)
        self.memory = self.read_memory()
        self.planner = None
        
    def init_agents_as_needed(self):
        if not self.planner:
            self.log("Initializing Agent Framework")
            self.planner = PlanningAgent(self.vector_db)
            self.log("Agent Framework is ready")
            
    def read_memory(self)->List[Opportunity]:
        if os.path.exists(self.MEMORY_FILE):
            with open(self.MEMORY_FILE,'r') as f:
                data = json.load(f)
                opportunities = [Opportunity(**item) for item in data]
                self.log(f"Agent Framework loaded {len(opportunities)} items from memory")
                return opportunities
        return []
    
    def write_memory(self)->None:
        data = [opportunity.model_dump() for opportunity in self.memory]
        with open(self.MEMORY_FILE, "w") as file:
            json.dump(data, file, indent=4)
    
    def log(self, message:str):
        text = BG_BLUE + WHITE + "[Agent Framework] " + message + RESET
        logging.info(text)
        
    def run(self)-> List[Opportunity]:
        self.init_agents_as_needed()
        logging.info("Kicking off Planning Agent")
        result = self.planner.plan(memory=self.memory)
        if result:
            self.memory.append(result)
            self.write_memory()
        return self.memory
    
    
    @classmethod
    def get_plot_data(cls,max_datapoints=10_000):
        vectors = joblib.load('vectors.pkl')
        documents = joblib.load('documents.pkl')
        categories = joblib.load('categories.pkl')
        colors = [COLORS[CATEGORIES.index(c)] for c in categories]
        tsne = TSNE(n_components=3, random_state=42, n_jobs=-1)
        reduced_vectors = tsne.fit_transform(vectors)
        return documents, reduced_vectors, colors
        
if __name__=="__main__":
    DealAgentFramework().run()