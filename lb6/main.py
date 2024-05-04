import csv
import tkinter as tk
from tkinter import filedialog, messagebox

from CollectiveDecision import CollectiveDecision

default_font = ("Helvetica", 10)


class App:
    def __init__(self, root: tk.Tk):
        self.cd = CollectiveDecision()

        self.btn_select_file = None
        self.entry_voters = None
        self.root = root
        self.root.title("Колективне прийняття рішень")

        self.init_window()

    def init_window(self):
        self.draw_collect_data()

    def draw_collect_data(self):
        self.clear_window()

        label_voters = tk.Label(self.root, text="Кількість голосуючих:")
        label_voters.pack(side=tk.TOP, padx=10, pady=5)

        self.entry_voters = tk.Entry(self.root)
        self.entry_voters.pack(side=tk.TOP, padx=10, pady=5)
        self.entry_voters.insert(0, "100")

        self.btn_select_file = tk.Button(self.root, text="Обрати CSV файл", command=self.load_csv)
        self.btn_select_file.pack(side=tk.TOP, padx=10, pady=5)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                csvreader = csv.reader(csvfile)
                data = list(csvreader)
                num_voters_text = self.entry_voters.get()
                if num_voters_text.isdigit():
                    num_voters = int(num_voters_text)
                    if len(data) != num_voters:
                        messagebox.showerror("Помилка", "Кількість рядків у файлі не співпадає з кількістю голосуючих.")
                        return
                else:
                    messagebox.showerror("Помилка", "Введіть коректну кількість голосуючих.")
                    return

        self.cd.process_data(data)

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    app.run()
