import logging

import src.a2a_server.infrastructure.adapter.mcp.mcp_client as mcp_client

#---------------------------------
# Configure logging
#---------------------------------
logger = logging.getLogger(__name__)

class Observer:
    
    def __init__(self):
        logger.info("Observer initialized SUCCESSFULLY")
    
    async def observe(self, product):
        logger.info("Observing product: %s", product)
        
        try:
            response = await mcp_client.resource_fetcher(product["sku"])
        except Exception as e:
            logger.error(f"Error fetching inventory service asynchronously: {e}")
            response = {"message": str(e)}
                            
        return response
