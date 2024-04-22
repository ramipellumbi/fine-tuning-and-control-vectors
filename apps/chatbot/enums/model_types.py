from enum import Enum


class ModelTypes(Enum):
    BASE: str = "Base"
    FINE_TUNED: str = "Fine Tuned"
    FINE_TUNED_AND_CV: str = "Fine Tuned & Control Vector"
