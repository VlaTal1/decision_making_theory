import numpy as np
from _consts import ALTERNATIVES

class AlternativeComparison:
    def __init__(self, criteria_name) -> None:
        self.criteria_name = criteria_name
        self.comparison_table = np.zeros((len(ALTERNATIVES), len(ALTERNATIVES)))
        self.self_vector = []
        self.weight_vector = []
