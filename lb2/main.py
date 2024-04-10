from Table import *
from utils import *

criteria = {
    "K1": ["k11", "k12", "k13"],
    "K2": ["k21", "k22", "k23"],
}

decisions = [1, 2, 1, 2, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2]


class App():
    def __init__(self, root):
        self.better = []
        self.worse = []
        self.incomparable = []
        self.alt_array = generate_alternatives(criteria)
        self.steps = []
        self.step_count = 0
        self.better_center = self.alt_array[0].value
        self.worse_center = self.alt_array[-1].value

        self.root = root
        self.root.title("Комбінації критеріїв")
        self.create_tabs()

    def make_decision(self, best_index):
        if decisions[self.step_count] == 1:
            for index, curr_alt in enumerate(self.alt_array[1:-1]):
                compare_to_np = self.alt_array[best_index].get_np_value()
                curr_alt_np = curr_alt.get_np_value()
                compare = curr_alt_np <= compare_to_np
                if all(compare):
                    curr_alt.class_number = "1"
        elif decisions[self.step_count] == 2:
            for index, curr_alt in enumerate(self.alt_array[best_index:-1], start=best_index):
                compare_to_np = self.alt_array[best_index].get_np_value()
                curr_alt_np = curr_alt.get_np_value()
                compare = curr_alt_np >= compare_to_np
                if all(compare):
                    curr_alt.class_number = "2"
        else:
            raise ValueError("decision class number can only be 1 or 2")

        self.step_count += 1

    def recalculate_class_centers(self):
        new_better_center = np.zeros(len(self.better_center), dtype=int)
        better_count = 0
        new_worse_center = np.zeros(len(self.worse_center), dtype=int)
        worse_count = 0
        for index, alt in enumerate(self.alt_array):
            if alt.class_number == "1":
                alt_np = alt.get_np_value()
                new_better_center += alt_np
                better_count += 1
            elif alt.class_number == "2":
                alt_np = alt.get_np_value()
                new_worse_center += alt_np
                worse_count += 1

        self.better_center = new_better_center / better_count
        self.worse_center = new_worse_center / worse_count

    def is_all_alternatives_have_class(self):
        class_count = 0
        for a in self.alt_array:
            if a.is_has_class():
                class_count += 1
        if class_count == len(self.alt_array):
            return True

    def create_tabs(self):
        notebook = ttk.Notebook(self.root)
        while True:
            table = Table(copy.deepcopy(self.alt_array),
                          self.better_center, self.worse_center)
            is_done = table.process()
            max_index = table.find_max_first_index()
            self.make_decision(max_index)
            self.recalculate_class_centers()
            tab = ttk.Frame(notebook)
            notebook.add(tab, text=f"Step {self.step_count}")
            table.create_table(list(criteria.keys()), tab)
            if is_done:
                break

        notebook.pack(expand=True, fill=tk.BOTH)

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
