import logging
from agents.agent import Agent
from agents.openai_agent import OpenAIAgent
from agents.pricer_agent import PricerAgent
from agents.random_forest_agent import RandomForestAgent
import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression

class EnsembleAgent(Agent):
    
    name = "Ensemble Agent"
    color = Agent.YELLOW
    
    def __init__(self,vector_db):
        
        self.log("Initializing Ensemble Agent")
        self.openai_agent = OpenAIAgent(vector_db)
        self.pricer_agent = PricerAgent()
        self.random_forest =  RandomForestAgent()
        self.model = joblib.load('ensemble_model.pkl')
        self.log("Ensemble Agent is ready")
        
    def price(self, desc:str)->float:
        
        self.log("Running Ensemble Agent - collaborating with specialist, frontier and random forest agents")
        openai_price = self.openai_agent.price(desc)
        pricer_price = self.pricer_agent.price(desc)
        random_forest_price = self.random_forest.price(desc)
        X = pd.DataFrame({
            'Openai': openai_price,
            'Prices Fine Tuned': pricer_price,
            'RandomForest': random_forest_price,
            'Min': [min(openai_price, pricer_price, random_forest_price)],
            'Max': [max(openai_price, pricer_price, random_forest_price)],
        })
        y_hat = max(0,self.model.predict(X)[0])
        self.log(f"Ensemble Agent complete - returning ${y_hat:.2f}")

        return y_hat