import logging
from agents.agent import Agent
from pinecone import Pinecone
from openai import OpenAI
import os
from dotenv import load_dotenv
from items import Item
import re
import math
import json
from sentence_transformers import SentenceTransformer
from datasets import load_dataset

class OpenAIAgent(Agent):
    
    name = "Openai Agent"
    color = Agent.BLUE
    
    MODEL = "gpt-4o-mini"   
    
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY") 
    pinecone_api_key = os.getenv("PINCECONE_API_KEY")
    def __init__(self,vector_db):
        
        self.log("Intializing OpenAI Agent")
        self.client = OpenAI(api_key=self.openai_api_key)
        self.vector_db = vector_db
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.log("Openai Agent is ready")

    def make_context(self,similars, prices):
        
        message = "To provide some context, here are some other items that might be similar to the item you need to estimate.\n\n"
        for similar, price in zip(similars, prices):
            message += f"Potentially related product:\n{similar}\nPrice is ${price:.2f}\n\n"
        return message
    
    def find_similars(self,descrip):
        vector = self.embedding_model.encode(descrip).tolist()
        results = self.vector_db.query(vector=vector, top_k=5, include_metadata=True)['matches']
        documents = [m['metadata']['description'] for m in results]
        prices = [m['metadata']['price'] for m in results]
        return documents, prices
    
    def get_price(self, s):
        
        s = s.replace('$','').replace(',','')
        match = re.search(r"[-+]?\d*\.\d+|\d+", s)
        return float(match.group()) if match else 0.0
    
    def message_for(self, desc , similars, prices):
        system_message = "You estimate prices of items. Reply only with the price, no explanation"
        user_prompt = self.make_context(similars, prices)
        user_prompt += "And now the question for you:\n\n"
        user_prompt += "How much does this cost?\n\n" + desc
        return [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": "Price is $"}
        ]
    
    def price(self, desc):
        
        documents, prices = self.find_similars(desc)
        self.log("Openai Ai Agent is going to predict the price with context of 5 similar prodoct")
        response = self.client.chat.completions.create(
            model=self.MODEL,
            messages=self.message_for(desc, documents, prices),
            seed=42,
            max_tokens=5
        )
        reply = response.choices[0].message.content
        result = self.get_price(reply)
        self.log(f"Openai Agent completed - predicting ${result:.2f}")
        return result

        