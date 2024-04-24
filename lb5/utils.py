import numpy as np


def check_for_zeros(arr):
    # Перевірка, чи є нулі в масиві
    if np.any(arr == 0):
        return True
    else:
        return False
