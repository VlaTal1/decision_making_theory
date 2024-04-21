import itertools
import numpy as np
from typing import Dict, List, Tuple
from itertools import combinations


# TODO move to MultiCriteria if only one usage
def transform_to_indices(dict: Dict[str, any]) -> Dict[str, np.ndarray[int, np.dtype]]:
    return {criterion: np.array([np.where(values == value)[0][0] for value in values], dtype=int) for
            criterion, values in dict.items()}


def array_to_index_dict(array: List[any]) -> Dict[int, any]:
    dict = {}
    for i, value in enumerate(array):
        dict[i] = value
    return dict


def array_to_none_dict(array):
    none_dict = {}
    for value in array:
        none_dict[value] = None
    return none_dict


def product(array):
    all_combinations = []

    for r in range(1, len(array) + 1):
        all_combinations.extend(list(combinations(array, r)))

    return all_combinations


def split_dictionary(original_dictionary):
    half_size = len(original_dictionary) // 2
    first_half = {}
    second_half = {}
    current_count = 0

    for key, value in original_dictionary.items():
        if current_count < half_size:
            first_half[key] = value
        else:
            second_half[key] = value
        current_count += 1

    return first_half, second_half


def recalculate_comparison_dict(comparison_dict, comb, sign):
    for comparison in comparison_dict.keys():
        if comparison != comb:
            if sign == '>':
                if comparison[0] == comb[0] and comparison[1] >= comb[1]:
                    comparison_dict[comparison] = '>'
            elif sign == '<':
                if comparison[0] >= comb[0] and comparison[1] == comb[1]:
                    comparison_dict[comparison] = '<'

    return comparison_dict


def create_graph(dict_refs, comparison_dict):
    graph = {key: [] for key in dict_refs.keys()}

    ref1, ref2 = split_dictionary(dict_refs)

    for i, key in enumerate(ref1.keys(), start=0):
        if i + 1 < len(ref1):
            graph[i].append(i + 1)

    for i, key in enumerate(ref2.keys(), start=len(ref2)):
        if i + 1 < len(ref1) + len(ref2):
            graph[i].append(i + 1)

    for key, value in comparison_dict.items():
        if value == '>':
            graph[key[0]].append(key[1])
        elif value == '<':
            graph[key[1]].append(key[0])

    return graph


def combinations(array1, array2):
    combinations = []
    for elem1 in array1:
        for elem2 in array2:
            combinations.append((elem1, elem2))
    return combinations


def dfs(graph, node, visited, current_path, longest_path):
    visited[node] = True
    current_path.append(node)

    for neighbor in graph[node]:
        if not visited[neighbor]:
            dfs(graph, neighbor, visited, current_path, longest_path)

    if len(current_path) > len(longest_path):
        longest_path[:] = current_path[:]

    current_path.pop()
    visited[node] = False


def find_longest_path(graph):
    visited = {node: False for node in graph}
    longest = []

    for node in graph:
        current_path = []
        dfs(graph, node, visited, current_path, longest)

    return longest


def compose_arrays_to_graph(arrays):
    graph = {}
    for array in arrays:
        for i in range(len(array) - 1):
            current_node = array[i]
            next_node = array[i + 1]
            if current_node not in graph:
                graph[current_node] = []
            if next_node not in graph[current_node]:
                graph[current_node].append(next_node)
        # Добавляем связь для последнего узла в массиве
        last_node = array[-1]
        if last_node not in graph:
            graph[last_node] = []
    return graph
