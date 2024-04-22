from enum import Enum


class ModelTypes(Enum):
    BASE = "Base"
    FINE_TUNED = "Fine Tuned"
    FINE_TUNED_AND_CV = "Fine Tuned & Control Vector"
