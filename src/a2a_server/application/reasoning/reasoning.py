import logging

from src.a2a_server.domain.dto.model import Decision
from src.a2a_server.domain.dto.state import InventoryState

# -------------------------------    
"""
    Reasoning Engine
    Responsible for:

    receiving inventory state
    analyzing inventory state
    making decisions
    returning the decision
"""
# ---------------------------------

#---------------------------------
# Configure logging and tracer
#---------------------------------
logger = logging.getLogger(__name__)

class Decider:

    def __init__(self):
        logger.info("Decider initialized SUCCESSFULLY")
        
    def decide(self, state: InventoryState) -> Decision:
        logger.info("Deciding action based on inventory state: %s", state)
        
        if state.stock <= state.minimum_stock:
            return Decision(
                action="HALT",
                reason="stock below minimum threshold"
            )

        if state.stock >= state.replenishment_threshold:
            return Decision(
                action="CONTINUE",
                reason="stock is healthy"
            )

        return Decision(
            action="MONITOR",
            reason="stock is within normal range"
        )