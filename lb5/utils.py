from typing import List

import numpy as np

from AlternativeComparison import AlternativeComparison
from _consts import CRITERIA


def check_for_zeros(arr):
    # Перевірка, чи є нулі в масиві
    if np.any(arr == 0):
        return True
    else:
        return False


def init_alternative_comparisons() -> List[AlternativeComparison]:
    comparisons = []
    for criterion in CRITERIA:
        comparisons.append(AlternativeComparison(criterion))
    return comparisons
