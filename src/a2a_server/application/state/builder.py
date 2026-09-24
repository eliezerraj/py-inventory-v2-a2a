import logging

import src.a2a_server.infrastructure.adapter.mcp.mcp_client as mcp_client

from src.a2a_server.config.settings import settings

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
        
    async def buildstate(self, product: dict):
        logger.info("Building product state based on: %s", product)
        
        try:
            resource_uri = f"time_series_order_items://{product}?limit=10&offset=0" 
            response = await mcp_client.mcp_resource_fetcher(resource_uri,settings.MCP_SERVER_ORDER_URL)
        except Exception as e:
            logger.error(f"Error fetching order service asynchronously: {e}")
            response = {"message": str(e)}
                            
        return response