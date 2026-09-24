import logging
import os

from typing import Dict

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

from src.a2a_server.config.settings import settings

logger = logging.getLogger(__name__)

# 1. Embedded MCP Resource Fetcher
async def resource_fetcher(sku: str) -> str:
    
    logger.info("Initialized resource_fetcher successfully.")
    logger.info("Fetching product resource for SKU: %s", sku)
    
    mcp_server_inventory_url = settings.MCP_SERVER_INVENTORY_URL
    mcp_server_order_url = settings.MCP_SERVER_ORDER_URL
    
    # Establish HTTP connection to the MCP server
    try:
        async with streamable_http_client(mcp_server_inventory_url) as (read_stream, write_stream):
            logger.info("Connected to MCP server at URL: %s", mcp_server_inventory_url)

            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()

                resource_uri = f"product://{sku}"
                logger.info("Fetching resource for URI: %s", resource_uri)

                result = await session.read_resource(resource_uri)
                return result.contents[0].text
    except Exception as e:
        logger.error("Exception occurred while fetching product resource for SKU: %s, error: %s", sku, e)
        raise

# 2. Embedded MCP Tool execution
async def tool_execution(payload: Dict) -> Dict:
    
    logger.info("Initialized tool_execution successfully.")
    logger.info("Executing tool for product with payload: %s", payload)
    
    mcp_server_inventory_url = settings.MCP_SERVER_INVENTORY_URL
    
    #headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}
    # Establish HTTP connection to the MCP server
    try:
        async with streamable_http_client(mcp_server_inventory_url) as (read_stream, write_stream):
            logger.info("Connected to MCP server at URL: %s", mcp_server_inventory_url)

            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()

                tool_uri = "patch_product"
                logger.info("Executing tool for URI: %s", tool_uri)

                result = await session.call_tool(tool_uri, payload)
                return result.contents[0].text
    except Exception as e:
        logger.error("Exception occurred while executing tool for product with payload: %s, error: %s", payload, e)
        raise
       
async def mcp_resource_fetcher(resource_uri: str, mcp_server_url: str) -> str:
    logger.info("Initialized mcp_resource_fetcher successfully.")
    logger.info("Fetching product resource for URI: %s", resource_uri)
        
    # Establish HTTP connection to the MCP server
    try:
        async with streamable_http_client(mcp_server_url) as (read_stream, write_stream):
            logger.info("Connected to MCP server at URL: %s", mcp_server_url)

            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()

                logger.info("Fetching resource for URI: %s", resource_uri)

                result = await session.read_resource(resource_uri)
                return result.contents[0].text
    except Exception as e:
        logger.error("Exception occurred while fetching product resource for URI: %s, error: %s", resource_uri, e)
        raise