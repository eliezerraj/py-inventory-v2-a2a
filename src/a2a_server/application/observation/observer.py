import logging

import src.a2a_server.infrastructure.adapter.mcp.mcp_client as mcp_client

from opentelemetry import trace
from src.a2a_server.config.settings import settings

#---------------------------------
# Configure logging
#---------------------------------
tracer = trace.get_tracer(__name__)
logger = logging.getLogger(__name__)

class Observer:
    
    def __init__(self):
        logger.info("Observer initialized SUCCESSFULLY")
    
    async def observe(self, product):
        logger.info("Observing product: %s", product)
        with tracer.start_as_current_span("observer.observe"):
            try:
                resource_uri = f"product://{product["sku"]}"
                response = await mcp_client.mcp_resource_fetcher(resource_uri, settings.MCP_SERVER_INVENTORY_URL)
            except Exception as e:
                logger.error(f"Error fetching inventory service asynchronously: {e}")
                response = {"message": str(e)}
                            
        return response
