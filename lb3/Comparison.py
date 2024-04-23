import numpy as np

class Comparison:
    def __init__(self, criteria, dict_refs, comparison_dict, comparison_graph, longest_path) -> None:
        self.criteria = criteria
        self.dict_refs = dict_refs
        self.comparison_dict = comparison_dict
        self.comparison_graph = comparison_graph
        self.longest_path = longest_path

    def __str__(self) -> str:
        return f'''Criteria: {self.criteria}
Reference dictionary: {self.dict_refs}
Comparison dictionary: {self.comparison_dict}
Comparison graph: {self.comparison_graph}
Longest path: {self.longest_path}
'''

    def longest_path_to_refs(self):
        return [self.dict_refs[value] for value in self.longest_path]
    
    def get_longest_path_refs_str(self):
        longest_path_refs = self.longest_path_to_refs()
        refs_str = []
        for path in longest_path_refs:
            refs_str.append(''.join(map(str, path)))
        return refs_str