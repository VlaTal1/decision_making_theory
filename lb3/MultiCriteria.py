import itertools
import numpy as np
from typing import Dict, List, Tuple
from utils import *


class MultiCriteria:
    def __init__(self, criteria: Dict[str, np.ndarray[int, str]], alternatives: Dict[str, np.ndarray[int, str]]):
        self.criteria = criteria
        self.orig_alternatives = alternatives
        self.alternatives = self.alternatives_to_values()
        self.transformed_criteria = transform_to_indices(self.criteria)
        self.first_ref = self.create_first_reference_situation()
        self.criterion_pairs = self.comparisons(list(self.first_ref.keys()))

    def alternatives_to_values(self):
        converted_dict = {}
        for alt, indices in self.orig_alternatives.items():
            values = [self.criteria[key][index] for key, index in zip(self.criteria.keys(), indices)]
            converted_dict[alt] = np.array(values)
        return converted_dict

    def alternatives_to_indices(self) -> Dict[str, np.ndarray[int, np.dtype]]:
        transformed_alternatives = {}
        for key, values in self.alternatives.items():
            indices = []
            for i, value in enumerate(values):
                for j, criterion_value in enumerate(self.criteria[list(self.criteria.keys())[i]]):
                    if criterion_value == value:
                        indices.append(j)
            transformed_alternatives[key] = np.array(indices)

        return transformed_alternatives

    def create_first_reference_situation(self):
        first_reference_situation = {}

        for i, item in enumerate(self.transformed_criteria.items()):
            key = item[0]
            values = item[1]
            reference_situations = []
            for j, value in enumerate(values):
                mask = np.zeros(
                    len(self.transformed_criteria.keys()), dtype=int)
                mask[i] = j
                reference_situations.append(mask)
            first_reference_situation[key] = np.array(reference_situations)

        return first_reference_situation

    def comparison_numbers(self):
        return len(self.criteria) * (len(self.criteria) - 1) / 2

    def comparisons(self, values):
        combinations = []
        for i in range(len(values)):
            for j in range(i+1, len(values)):
                combinations.append([values[i], values[j]])

        return np.array(combinations)

    def get_first_ref_by_key(self, key):
        return self.first_ref[key]
    
    def compose_final_array(self, first_vector_score, vector_score):
        new_first_vector_score = first_vector_score.copy()
        new_first_vector_score += 1
        first_vector_score_str = ''.join(map(str, new_first_vector_score))

        vector_score_str = ''.join(map(str, vector_score))

        sorted_vector_score = np.array(vector_score)
        sorted_vector_score = np.sort(sorted_vector_score)
        sorted_vector_score_str = ''.join(map(str, sorted_vector_score))

        return [first_vector_score_str, vector_score_str, sorted_vector_score_str]

    def calculate_final_table(self, final_path):
        table = {}
        for key, values in self.orig_alternatives.items():
            vector_score = []
            for i, value in enumerate(values):
                for j, ref in enumerate(final_path):
                    ref_array = [int(char) for char in ref]
                    if ref_array[i] == value:
                        vector_score.append(j + 1)
                        break
            table[key] = self.compose_final_array(values, vector_score)
        return table

