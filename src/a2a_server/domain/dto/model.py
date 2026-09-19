from typing import Optional
from pydantic import BaseModel

class Product(BaseModel):
    sku: str = None
    name: str = None
    description: str = None
    price: float = None
    stock: int = None

class Decision(BaseModel):
    action: str = None
    reason: str= None
    
class InventoryState(BaseModel):
    sku: str = None
    trend: str = None
    stock: int = None
    price: float = None
    minimum_stock: int = None
    replenishment_threshold: int = None
    
class AgentGoal(BaseModel):
    goal: str = None
    sku: str = None
    objective: str = None
    action: str = None
    parameters: dict = None