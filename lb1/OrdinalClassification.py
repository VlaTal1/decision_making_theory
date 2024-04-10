from typing import Dict, List, Tuple

import numpy as np
import itertools


class OrdinalClassification:

    def __init__(self, criteria: Dict[str, np.ndarray[str, np.dtype]], chosen_alternative_index: int):
        self.criteria = criteria
        self.chosen_alternative_index = chosen_alternative_index
        self.alternatives = self.create_alternatives() 

        self.better = []
        self.worse = []
        self.incomparable = []

    def transform_criteria_to_indices(self) -> Dict[str, np.ndarray[int, np.dtype]]:
        return {criterion: np.array([np.where(values == value)[0][0] for value in values], dtype=int) for
                criterion, values in self.criteria.items()}

    def create_alternatives(self) -> List[np.ndarray[int, np.dtype]]:
        transformed_criteria = self.transform_criteria_to_indices()

        transformed_values = list(transformed_criteria.values())
        return [np.array(combo) for combo in itertools.product(*transformed_values)]

    def compare_alternatives(self,
                             chosen: np.ndarray[int, np.dtype],
                             compare_to: np.ndarray[int, np.dtype],
                             compare_to_index: int) -> str:
        if compare_to_index == self.chosen_alternative_index:
            return "chosen"
        elif compare_to_index < self.chosen_alternative_index:
            compare = compare_to <= chosen
            return "better" if all(compare) else "incomparable"
        elif compare_to_index > self.chosen_alternative_index:
            compare = compare_to >= chosen
            return "worse" if all(compare) else "incomparable"

    def get_best_alternative(self) -> Tuple:
        return tuple(self.criteria[key][index] for key, index in zip(self.criteria.keys(), self.alternatives[0]))

    def get_worst_alternative(self) -> Tuple:
        return tuple(self.criteria[key][index] for key, index in zip(self.criteria.keys(), self.alternatives[-1]))

    def hypothetical_amount(self) -> int:
        return np.prod([len(values) for values in self.criteria.values()])

    def calculate_all_alternatives(self) -> int:
        amount = len(self.better) + len(self.worse) + len(self.incomparable) + 1
        return amount

    def get_criteria_keys(self) -> List[str]:
        return list(self.criteria.keys())

    def criteria_values_by_indices(self, indices: np.ndarray[int, np.dtype]) -> List[str]:
        return [self.criteria[key][index] for key, index in zip(self.get_criteria_keys(), indices)]

    def process(self):
        chosen_alternative = self.alternatives[self.chosen_alternative_index - 1]

        for i, alternative in enumerate(self.alternatives, start=1):
            comparison = self.compare_alternatives(chosen_alternative, alternative, i)
            if comparison == "better":
                self.better.append(alternative)
            elif comparison == "worse":
                self.worse.append(alternative)
            elif comparison == "chosen":
                pass
            elif comparison == "incomparable":
                self.incomparable.append(alternative)
