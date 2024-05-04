from pprint import pprint as pp
from RelativeMajority import RelativeMajority
from AbsoluteMajority import AbsoluteMajority
from BordRule import BordRule


class CollectiveDecision:
    def __init__(self):
        self.original_data = None
        self.voting_profile = {}

        self.rm = None
        self.am = None
        self.br = None

    def process_data(self, data):
        self.original_data = data

        for row in data:
            row_tuple = tuple(row)
            if row_tuple in self.voting_profile:
                self.voting_profile[row_tuple] += 1
            else:
                self.voting_profile[row_tuple] = 1

        print(len(self.voting_profile))
        pp(self.voting_profile)

        self.rm = RelativeMajority(self.voting_profile)
        self.am = AbsoluteMajority(self.voting_profile)
        self.br = BordRule(self.voting_profile)
