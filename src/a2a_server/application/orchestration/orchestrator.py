import logging

from src.a2a_server.application.observation.observer import Observer
from src.a2a_server.application.state.builder import Builder
from src.a2a_server.application.reasoning.decider import Decider

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
        self.decider = Decider()

    async def observe(self, payload):
        logger.info(f"observe payload.: payload={payload}")
        with tracer.start_as_current_span("orchestrator.observe"): 
            response = await self.observer.observe(payload["product"])
            return response

    async def state(self, payload):
        logger.info(f"state payload.: payload={payload}")
        with tracer.start_as_current_span("orchestrator.state"):
            response = await self.buildstate.buildstate(payload["product"])
            return response

    async def reasoning(self, payload):
        logger.info(f"reasoning payload.: payload={payload}")
        with tracer.start_as_current_span("orchestrator.reasoning"):
            
            response = await self.decider.reasoning(payload["product_state"])
            
            return response
           
    async def monitor(self, payload):
        logger.info(f"monitor payload.: payload={payload}")
        with tracer.start_as_current_span("orchestrator.monitor"):
            
            response_observed = await self.observer.observe(payload["product"])
            
            response_state = await self.buildstate.buildstate(payload["product"])

            decider_payload = {
                "observed": response_observed,
                "state": response_state
            }

            #response_reasoning = await self.decider.reasoning(decider_payload)
            
            response = {
                "observed": response_observed,
                "state": response_state,
                "action": "action taken"
            }

            return response