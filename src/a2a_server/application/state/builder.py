import logging
import asyncio

import src.a2a_server.infrastructure.adapter.mcp.mcp_client as mcp_client
import src.a2a_server.infrastructure.adapter.a2a.a2a_client as a2a_client
from src.a2a_server.infrastructure.adapter.a2a.a2a_client import A2aRequest

from src.a2a_server.config.settings import settings

from opentelemetry import trace
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
tracer = trace.get_tracer(__name__)
logger = logging.getLogger(__name__)

class Builder:

    def __init__(self):
        self.a2a_adapter = a2a_client.A2aAdapter()
        logger.info("Builder initialized SUCCESSFULLY")
        
    async def buildstate(self, product: dict):
        logger.info("Building product state based on: %s", product)
        
        try:
            resource_uri = f"time_series_order_items://{product}?limit=10&offset=0" 
            response = await mcp_client.mcp_resource_fetcher(resource_uri,settings.MCP_SERVER_ORDER_URL)

            request = A2aRequest(
                endpoint=settings.A2A_SERVER_STATISTIC_A2A_URL,
                skill="statistics.compute",
                payload={
                    "data": [100,200,100,300]
                }
            )
            
            response_state = await self.a2a_adapter.call(request)
            
            print("===================== Response state before JSON conversion:", response_state.message.parts)

            statistics_text = None
            if response_state and response_state.HasField("message"):
                for part in response_state.message.parts:
                    if part.HasField("text"):
                        statistics_text = part.text
                        break
            
        except Exception as e:
            logger.error(f"Error fetching order service asynchronously: {e}")
            response_state = {"message": str(e)}
                  
        return statistics_text