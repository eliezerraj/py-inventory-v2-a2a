from typing import Optional
from pydantic import BaseModel

class Statistic(BaseModel):
    population: Optional[list[float]] = None
    
    count: Optional[int] = None
    mean: Optional[float] = None
    std: Optional[float] = None
    slope: Optional[float] = None
