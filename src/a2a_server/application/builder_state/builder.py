import logging

from src.a2a_server.domain.dto.model import Decision
from src.a2a_server.domain.dto.state import InventoryState

# -------------------------------    
"""
    Builder
    Responsible for:

    receiving inventory observation data
    building the inventory state
    returning the built inventory state
"""
# ---------------------------------

#---------------------------------
# Configure logging and tracer
#---------------------------------
logger = logging.getLogger(__name__)

class Builder:

    def __init__(self):
        logger.info("Builder initialized SUCCESSFULLY")
        
    def build(self, observation: dict) -> InventoryState:
        logger.info("Building inventory state based on observation: %s", observation)
        
        inventory_state = InventoryState(
            sku=observation.get("sku", ""),
            name=observation.get("name", ""),
            description=observation.get("description", ""),
            price=observation.get("price", 0.0),
            stock=observation.get("stock", 0),
            minimum_stock=observation.get("minimum_stock", 0),
            replenishment_threshold=observation.get("replenishment_threshold", 0)
        )

        return Decision(
            action="MONITOR",
            reason="stock is within normal range"
        )