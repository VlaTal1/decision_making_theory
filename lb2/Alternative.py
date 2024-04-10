import copy

import numpy as np


class Alternative:
    def __init__(self, class_number, value):
        self.class_number = class_number
        self.value = value

    def get_np_value(self) -> np.ndarray:
        return np.array(self.value, dtype=int)

    def is_has_class(self):
        if self.class_number == "1" or self.class_number == "2":
            return True
        else:
            return False

    def __deepcopy__(self, memo):
        copied_obj = Alternative(copy.deepcopy(self.class_number, memo),
                                 copy.deepcopy(self.value, memo))
        return copied_obj
