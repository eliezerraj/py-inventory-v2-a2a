import logging

from src.a2a_server.application.observation.observer import Observer
from src.a2a_server.application.state.builder import Builder

from opentelemetry import trace

# --------------------------------
"""
InventoryOrchestrator

Responsible for:

coordinating the steps
retrieving state
calling the decision engine
executing the selected action
verifying the result
"""
#---------------------------------

#---------------------------------
# Configure logging and tracer
#---------------------------------
tracer = trace.get_tracer(__name__)
logger = logging.getLogger(__name__)

class Orchestrator:
    
    def __init__(self):
        logger.info("Orchestrator initialized SUCCESSFULLY")
        
        self.observer = Observer()
        self.buildstate = Builder()

    async def observe(self, payload):
        logger.info(f"observe payload.: payload={payload}")
        
        response = await self.observer.observe(payload["product"])
        
        return response

    async def state(self, payload):
        logger.info(f"state payload.: payload={payload}")
        
        response = await self.buildstate.buildstate(payload["product"])
        
        return response
                
    def monitor(self, payload):
        logger.info(f"Handling monitor request.: payload={payload}")
        
        sku = payload
        logger.info(f"Monitoring product with SKU: {sku}")
        
        response = {"action": "action taken"}
        
        return response