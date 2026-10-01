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
    grid_metadata: dict = None
    
class Price(BaseModel):
    currency: str = None
    amount: float = None

class Inventory(BaseModel):
    available: int = None
    sold: int = None

class Statistics(BaseModel):
    count: int = None
    mean: float = None
    std: float = None
    slope: float = None
    norm_z: float = None

class ProductState(BaseModel):
    sku: str = None
    price: Price = None
    inventory: Inventory = None
    amount: Statistics = None
    count: Statistics = None

class AgentGoal(BaseModel):
    goal: str = None
    sku: str = None
    objective: str = None
    action: str = None
    parameters: dict = None