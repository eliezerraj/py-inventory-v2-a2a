import logging
import numpy as np
from a2a_server.domain.dto.model import Statistic

import opentelemetry.trace as trace

#---------------------------------
# Configure logging
#---------------------------------
tracer = trace.get_tracer(__name__)
logger = logging.getLogger(__name__)

def calc_slope(numbers):
    if numbers.size < 2:
        return 0.0

    x = np.arange(len(numbers))
    slope, _ = np.polyfit(x, numbers, 1)
    slope = float(slope)
    return slope if np.isfinite(slope) else 0.0

def compute_statistics(list_values: list[float]) -> Statistic:
    with tracer.start_as_current_span("domain.usecase.compute_statistics"):
        logger.info("def.compute_statistics()" , extra={"list_values": list_values})    

        if not list_values:
            logger.warning("No values enough provided for statistical computation.")
            return Statistic()
        
        # Ensure we operate on a float numpy array
        tps_values = np.array(list_values, dtype=float)
        n = tps_values.size
        
        mean = float(np.mean(tps_values))
        std_dev = float(np.std(tps_values))
        slope = calc_slope(tps_values)

        return Statistic(
            #population= list_values,
            mean=mean,
            std=std_dev,
            slope=slope,
            count=n
        )