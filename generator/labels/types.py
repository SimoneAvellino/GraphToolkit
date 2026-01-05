from enum import Enum


class LabelStrategyName(str, Enum):
    none = "none"
    random = "random"
    community = "community"


LABEL_STRATEGIES = LabelStrategyName
