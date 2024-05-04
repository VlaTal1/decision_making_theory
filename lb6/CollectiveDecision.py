from pprint import pprint as pp


class CollectiveDecision:
    def __init__(self):
        self.original_data = None
        self.voting_profile = {}

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
