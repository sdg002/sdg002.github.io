from enum import Enum


class StoppingCriteria(Enum):
    """Defines an approach for stopping the further discovery of RANSAC lines/circles."""
    MAX_OBJECTS = "max_objects"
    RANSAC_THRESHOLD_SPIKE = "ransac threshold spike"
    
    