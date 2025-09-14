import modal
from agents.agent import Agent

class PricerAgent(Agent):
    name = "Pricer Agent"
    color = Agent.RED
    
    
    def __init__(self):
        self.log("Pricer Agent initialized - connecting to modal")
        
        Pricer = modal.Cls.from_name("pricer-service", "Pricer")
        self.pricer = Pricer()
        self.log("Pricer Agent is ready")
        
    def price(self, item_description: str) -> str:
        self.log("Pricer Agent is calling remote fine-tuned model")
        
        price = self.pricer.price.remote(item_description)
        self.log(f"Received price: {price}")
        return price