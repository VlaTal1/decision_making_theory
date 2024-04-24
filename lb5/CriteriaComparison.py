import numpy as np
from _consts import CRITERIA

class CriteriaComparison:
    def __init__(self):
        self.criteria_comparisons = np.zeros((len(CRITERIA), len(CRITERIA)))
        self.self_vector = []
        self.criteria_weight = []