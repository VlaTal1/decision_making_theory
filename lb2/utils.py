from Alternative import *
from typing import List


def transform_criteria_to_indices(criteria):
    transformed_criteria = {}

    for criterion, values in criteria.items():
        indices = [values.index(value) for value in values]
        transformed_criteria[criterion] = indices

    return transformed_criteria


def generate_index_combinations(transformed_criteria):
    criteria_keys = list(transformed_criteria.keys())
    criteria_values = [transformed_criteria[key] for key in criteria_keys]

    def cartesian_product(current_index=0, current_combo=[]):
        if current_index == len(criteria_values):
            return [current_combo[:]]

        result = []
        for value in criteria_values[current_index]:
            current_combo.append(value)
            result.extend(cartesian_product(current_index + 1, current_combo))
            current_combo.pop()

        return result

    result = cartesian_product()

    return result


def index_combinations_to_alt_arr(index_combinations):
    alt_array = [Alternative("1", index_combinations[0])]
    for combination in index_combinations[1:-1]:
        alt_array.append(Alternative("1, 2", combination))
    alt_array.append(Alternative("2", index_combinations[-1]))
    return alt_array


def generate_alternatives(criteria) -> List[Alternative]:
    transformed_criteria = transform_criteria_to_indices(criteria)
    index_combinations = generate_index_combinations(transformed_criteria)
    return index_combinations_to_alt_arr(index_combinations)


def calculate_distance(alternative: list, class_center: list):
    distance = 0
    for alt_value, class_value in zip(alternative, class_center):
        distance += abs(alt_value - class_value)

    return distance


def calculate_proximity_measure(max_d, d1, d2, first_d):
    if first_d == 1:
        return (max_d - d1) / (max_d - d1 + max_d - d2)
    elif first_d == 2:
        return (max_d - d2) / (max_d - d1 + max_d - d2)
    else:
        raise ValueError("first_d can only be 1 or 2")


def calculate_informativeness_to_class(p, g):
    return p * g


def calculate_informativeness(f1, f2):
    return f1 + f2
