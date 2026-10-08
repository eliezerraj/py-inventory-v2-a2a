import logging
import numpy as np

from src.a2a_server.application.action.action import Action
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
        self.action = Action()

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
            
            try:
                response_observed = await self.observer.observe(payload["product"])
                
                # Check if observer returned an error
                if response_observed.get("error"):
                    logger.warning(f"Observer error: {response_observed.get('message')}")
                    return {
                        "error": True,
                        "status_code": response_observed.get("status_code", 500),
                        "message": response_observed.get("message")
                    }
                
                response_state = await self.buildstate.buildstate(payload["product"])

                decider_payload = {
                    "product_state": {
                        "sku": payload["product"]["sku"],
                        "price": (response_observed.get("product") or {}).get("price"),
                        "inventory": (response_observed.get("product") or {}).get("inventory"),
                        "amount":{
                            "statistics": response_state.get("price", {}).get("statistics")
                        },
                        "count":{
                            "statistics": response_state.get("inventory", {}).get("statistics")
                        }
                    }
                }

                response_reasoning = await self.decider.reasoning(decider_payload)
                
                if "grid_metadata" not in response_reasoning.grid_metadata:
                    logger.error("Missing grid_metadata in response_reasoning.grid_metadata")
                    return {"error": "Missing grid_metadata in response_reasoning.grid_metadata, maybe the product not found"}
                
                if "current_state" not in response_reasoning.grid_metadata:
                    logger.error("Missing current_state in response_reasoning.grid_metadata")
                    return {"error": "Missing current_state in response_reasoning.grid_metadata, maybe the product not found"}
                
                current_state = np.array(response_reasoning.grid_metadata.get("current_state", [0.0, 0.0]))
                
                response_action = self.action.take_action(current_state=current_state)

                logger.info(f"Obtained response_action: {response_action}")

                response = {
                    "action": response_action,
                    "metadata": {
                        "observed": response_observed,
                        "state": response_state,
                        "reasoning": response_reasoning
                    }
                }

                return response
            
            except Exception as e:
                logger.error(f"Error in monitor: {e}")
                return {"error": str(e)}