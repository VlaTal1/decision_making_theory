import unittest
import numpy as np

from lb1.OrdinalClassification import OrdinalClassification


class TestOrdinalClassification(unittest.TestCase):

    def setUp(self):
        criteria = {
            "Criterion1": np.array(["Low", "Medium", "High"]),
            "Criterion2": np.array(["Good", "Average", "Bad"])
        }
        chosen_alternative_index = 5

        self.ord_class = OrdinalClassification(criteria, chosen_alternative_index)

    def test_transform_criteria_to_indices(self):
        expected = {
            "Criterion1": [0, 1, 2],
            "Criterion2": [0, 1, 2]
        }
        transformed = self.ord_class.transform_criteria_to_indices()

        # Convert NumPy arrays to lists
        transformed = {key: value.tolist() for key, value in transformed.items()}

        self.assertDictEqual(expected, transformed)

    def test_create_alternatives(self):
        expected = [
            np.array([0, 0]),
            np.array([0, 1]),
            np.array([0, 2]),
            np.array([1, 0]),
            np.array([1, 1]),
            np.array([1, 2]),
            np.array([2, 0]),
            np.array([2, 1]),
            np.array([2, 2])
        ]

        alternatives = self.ord_class.create_alternatives()

        for exp, alt in zip(expected, alternatives):
            self.assertTrue(np.array_equal(exp, alt))

    def test_compare_better_alternatives(self):
        chosen = np.array([1, 1])
        compare_to = np.array([0, 0])
        compare_to_index = 0
        self.assertEquals("better", self.ord_class.compare_alternatives(chosen, compare_to, compare_to_index))

    def test_compare_worse_alternatives(self):
        chosen = np.array([1, 1])
        compare_to = np.array([2, 2])
        compare_to_index = 9
        self.assertEquals("worse", self.ord_class.compare_alternatives(chosen, compare_to, compare_to_index))

    def test_compare_incomparable_alternatives(self):
        chosen = np.array([1, 1])
        compare_to = np.array([2, 0])
        compare_to_index = 7
        self.assertEquals("incomparable", self.ord_class.compare_alternatives(chosen, compare_to, compare_to_index))

    def test_compare_chosen_alternatives(self):
        chosen = np.array([1, 1])
        compare_to = np.array([1, 1])
        compare_to_index = 5
        self.assertEquals("chosen", self.ord_class.compare_alternatives(chosen, compare_to, compare_to_index))

    def test_get_best_alternatives(self):
        expected = ("Low", "Good")
        best_alternative = self.ord_class.get_best_alternative()
        self.assertEquals(expected, best_alternative)

    def test_get_worst_alternatives(self):
        expected = ("High", "Bad")
        best_alternative = self.ord_class.get_worst_alternative()
        self.assertEquals(expected, best_alternative)

    def test_hypothetical_amount(self):
        hypothetical_amount = self.ord_class.hypothetical_amount()
        self.assertEquals(9, hypothetical_amount)

    def test_calculate_all_alternatives(self):
        self.ord_class.process()
        all_alternatives_amount = self.ord_class.calculate_all_alternatives()
        self.assertEquals(9, all_alternatives_amount)

    def test_get_criteria_keys(self):
        expected = ["Criterion1", "Criterion2"]
        criteria_keys = self.ord_class.get_criteria_keys()
        self.assertEquals(expected, criteria_keys)

    def test_criteria_values_by_indices(self):
        expected = ["Low", "Average"]
        indices = np.array([0, 1])
        criteria_values = self.ord_class.criteria_values_by_indices(indices)
        self.assertEquals(expected, criteria_values)

    def test_process(self):
        expected_better = [
            np.array([0, 0]),
            np.array([0, 1]),
            np.array([1, 0])
        ]
        expected_worse = [
            np.array([1, 2]),
            np.array([2, 1]),
            np.array([2, 2])
        ]
        expected_incomparable = [
            np.array([0, 2]),
            np.array([2, 0])
        ]

        self.ord_class.process()

        for better_exp, better_alt in zip(expected_better, self.ord_class.better):
            self.assertTrue(np.array_equal(better_exp, better_alt))

        for worse_exp, worse_alt in zip(expected_worse, self.ord_class.worse):
            self.assertTrue(np.array_equal(worse_exp, worse_alt))

        for incomparable_exp, incomparable_alt in zip(expected_incomparable, self.ord_class.incomparable):
            self.assertTrue(np.array_equal(incomparable_exp, incomparable_alt))


if __name__ == "__main__":
    unittest.main()
