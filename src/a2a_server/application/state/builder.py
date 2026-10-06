import logging
import asyncio
import json

import src.a2a_server.infrastructure.adapter.mcp.mcp_client as mcp_client
import src.a2a_server.infrastructure.adapter.a2a.a2a_client as a2a_client
from src.a2a_server.infrastructure.adapter.a2a.a2a_client import A2aRequest
from src.a2a_server.domain.dto.model import Statistics

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
        logger.info("Building state based on: %s", product["sku"])
        with tracer.start_as_current_span("builder.buildstate"):

            statistics_available = None
            statistics_price = None
            response = None
        
            try:
                # Fetch order time series data from the MCP server asynchronously
                resource_uri = f"time_series_order_items://{product['sku']}?limit=10&offset=0" 
                response_order_time_series = await mcp_client.mcp_resource_fetcher(resource_uri, settings.MCP_SERVER_ORDER_URL)

                order_time_series = json.loads(response_order_time_series)
                time_series_data = order_time_series.get("time_series_order_items", {}).get("time_series_data", [])
                
                # Extract amounts and counts from the time series data            
                price = order_time_series.get("time_series_order_items", {}).get("product", {}).get("price", {}).get("amount", None)
                available = order_time_series.get("time_series_order_items", {}).get("product", {}).get("inventory", {}).get("available", None)
                
                # Extract amounts and counts from the time series data
                prices = [item["sum_amount"] for item in time_series_data if item.get("sum_amount") is not None]
                availables = [item["sum_quantity"] for item in time_series_data if item.get("sum_quantity") is not None]
                
                # ---------------------------------------------------
                # Compute amounts statistics using the A2A server
                # --------------------------------------------------
                reponse_count = A2aRequest(
                    endpoint=settings.A2A_SERVER_STATISTIC_A2A_URL,
                    skill="statistics.compute",
                    payload={
                        "data": availables
                    }
                )
                response_state_count = await self.a2a_adapter.call(reponse_count)
                
                if response_state_count and response_state_count.HasField("message"):
                    for part in response_state_count.message.parts:
                        if part.HasField("text"):
                            statistics_available = json.loads(part.text)
                            break
                # ---------------------------------------------------
                # Compute amounts statistics using the A2A server
                # ---------------------------------------------------
                reponse_amount = A2aRequest(
                    endpoint=settings.A2A_SERVER_STATISTIC_A2A_URL,
                    skill="statistics.compute",
                    payload={
                        "data": prices
                    }
                )
                response_state_amount = await self.a2a_adapter.call(reponse_amount)
                
                if response_state_amount and response_state_amount.HasField("message"):
                    for part in response_state_amount.message.parts:
                        if part.HasField("text"):
                            statistics_price = json.loads(part.text)
                            break

                # Compute normalized z-scores for the current price and available inventory
                statistics_price["norm_z"] = (price - statistics_price.get("mean")) / (statistics_price.get("std") if statistics_price.get("std") else 1) if statistics_price else None
                statistics_available["norm_z"] = (available - statistics_available.get("mean")) / (statistics_available.get("std") if statistics_available.get("std") else 1) if statistics_available else None

                statistics_price = Statistics(**statistics_price)
                statistics_available = Statistics(**statistics_available)
                        
            except Exception as e:
                logger.error(f"Error fetching order service asynchronously: {e}")
                response = {"message": str(e)}
                    
            response = {
                "product": product,
                "price": {
                    "current": price,
                    "statistics": statistics_price,
                    "data": prices
                },
                "inventory": {
                    "current": available,
                    "statistics": statistics_available,
                    "data": availables
                }
            }
            
            return response