import logging
import numpy as np
from opentelemetry import trace

from src.a2a_server.application.reasoning.gridcell import GridCellModule

from src.a2a_server.domain.dto.model import Decision, ProductState

#---------------------------------
# Configure logging and tracer
#---------------------------------
logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)

class Decider:

    def __init__(self):
        logger.info("Decider initialized SUCCESSFULLY")
        
        NUM_CEL = 64
        docs = np.linspace(-1, 1, NUM_CEL)
        slopes = np.linspace(-1, 1, NUM_CEL)
        X, Y = np.meshgrid(docs, slopes)

        # 2. Your Original Inventory Place Cells
        # Where i am and place cells are the sensors
        INVENTORY_PLACE_CELL = {
            "FULL":     {"coords": np.array([1.0, 0.2])},
            "HIGH":     {"coords": np.array([0.7, 0.5])},
            "BALANCED": {"coords": np.array([0.4, 0.8])},
            "LOW":      {"coords": np.array([0.2, 0.12]),},
            "CRITICAL": {"coords": np.array([0.1, 0.15]),},
            "RUNOUT":   {"coords": np.array([0.0, 0.2]),},
        }

        # 3 Set the Peak of the Grid Cell to the "BALANCED" Inventory Place Cell
        self.SCALE_COARSE = {"SHORT": 0.125, "MEDIUM": 0.25, "LONG": 0.5}
        self.SCALE_CHOICE = "MEDIUM"
        self.ANCHOR_CHOICE = "BALANCED"
        self.ANCHOR_COORD=INVENTORY_PLACE_CELL[self.ANCHOR_CHOICE]["coords"]

        # 4. Initialize Module and compute surface
        self.GRID_MODULE = GridCellModule(scale=self.SCALE_COARSE[self.SCALE_CHOICE], anchor_coord=self.ANCHOR_COORD, rng_seed=42)

        grid_firing = self.GRID_MODULE.get_grid_activation(X, Y)

        print("-----start grid firing-----------")
        print("grid_firing:" ,grid_firing)
        print("-----end grid firing-----------")

    def get_continuous_representation(self, current_state, anchor_coord):
        representations = {}
        representation = []

        for name in self.SCALE_COARSE:
            activation = self.GRID_MODULE.get_single_activation(current_state)

            representations[name] = float(activation)
            representation.append(float(activation))

        return representations, representation

    def get_direction_to_peak(self, current_state, peak_coord):
        direction = peak_coord - current_state

        distance = np.linalg.norm(direction)
        if distance > 0:
            direction_normalized = direction / distance
        else:
            direction_normalized = np.zeros_like(direction)

        return direction, direction_normalized, distance

    def generate_path_to_peak(self, current_state, peak_coord,steps=10):
        path = []

        for t in np.linspace(0.0, 1.0, steps):
            position = ( current_state + t * (peak_coord - current_state))
            path.append(position)
            
        return np.array(path)

    async def reasoning(self, product_state: ProductState) -> any:
        logger.info("Deciding action based on product state: %s", product_state)
        with tracer.start_as_current_span("decider.reasoning"):
            
            # Handle both dict and ProductState object
            if isinstance(product_state, dict):
                product_current_state = np.array([product_state['inventory_level'], product_state['amount_level']])
            else:
                product_current_state = np.array([product_state.inventory_level, product_state.amount_level])
            
            continuous_representation, g_representation = self.get_continuous_representation(
                current_state=product_current_state,
                anchor_coord=self.ANCHOR_COORD
            )

            print("-------------")
            print("Continuous representation:", continuous_representation)
            print("Representation:", g_representation)
            print("-------------")
            
            direction, direction_normalized, distance = self.get_direction_to_peak(
                current_state=product_current_state,
                peak_coord=self.ANCHOR_COORD
            )

            print("-------------")
            print("product_current_state:", product_current_state)
            print("Direction to peak:", direction)
            print("Normalized direction:", direction_normalized)
            print("Distance to peak:", self.ANCHOR_COORD ,distance)
            print("-------------")

            path = self.generate_path_to_peak(product_current_state, self.ANCHOR_COORD,steps=10)

            paths = []
            for i, position in enumerate(path):
                print(f"step={i:02d}",f"position={position}",f"grid={g_representation}" )
                print("-------------")
                paths.append({
                    "step": i,
                    "position": position.tolist(),
                })
        
            return Decision(
                grid_metadata={
                    "current_state": product_current_state.tolist(),
                    "peak_coord": self.ANCHOR_COORD.tolist(),
                    "direction": direction.tolist(),
                    "direction_normalized": direction_normalized.tolist(),
                    "distance": distance,
                    "continuous_representation": continuous_representation,
                    "scale": self.SCALE_CHOICE,
                    "paths": paths
                }
            )