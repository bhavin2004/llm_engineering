import os
from agents.deals import Opportunity
from agents.agent import Agent
import requests
from dotenv import load_dotenv

class MessagingAgent(Agent):
    
    name = "Messaging Agent"
    color = Agent.WHITE
    
    def __init__(self):
        self.log(f"Messaging Agent is initializing")
        load_dotenv()
        self.slack = os.getenv('SLACK_WEBHOOK_URL')
        self.log("Messaging Agent is ready")
        
    def message(self, text:str):
        self.log("Messaging Agent is sending a slack message")
        payload_form = {"content": text}
        response = requests.post(self.slack, json=payload_form)
        if response.status_code == 200:
            self.log("Messaging Agent sent the message successfully")
        else:
            self.log(f"Messaging Agent failed to send message: {response.content}")
            
    def alert(self,opportunity:Opportunity):
        text = f"Deal Alert! Price=${opportunity.deal.price:.2f}, "
        text += f"Estimate=${opportunity.estimate:.2f}, "
        text += f"Discount=${opportunity.discount:.2f}\n:"
        text += opportunity.deal.product_description[:100]+'...\n'
        text += opportunity.deal.url
        
        self.message(text)
        self.log("Messaging Agent has completed")
        

        
            
            

if __name__ == "__main__":
    agent = MessagingAgent()
    agent.message("Hello from Messaging Agent")