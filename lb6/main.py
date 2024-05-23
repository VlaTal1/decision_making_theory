import csv
import tkinter as tk
from tkinter import filedialog, messagebox

from CollectiveDecision import CollectiveDecision


class App:
    def __init__(self, root: tk.Tk):
        self.cd = CollectiveDecision()

        self.btn_select_file = None
        self.entry_voters = None
        self.root = root
        self.root.title("Колективне прийняття рішень")

        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.LEFT, fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.history_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.history_frame, anchor="nw")

        self.init_window()

    def init_window(self):
        self.draw_collect_data()

    def draw_collect_data(self):
        self.clear_window()

        label_voters = tk.Label(self.history_frame, text="Кількість голосуючих:")
        label_voters.pack(padx=10, pady=5, anchor=tk.W)

        self.entry_voters = tk.Entry(self.history_frame)
        self.entry_voters.pack(padx=10, pady=5, anchor=tk.W)
        self.entry_voters.insert(0, "34")

        self.btn_select_file = tk.Button(self.history_frame, text="Обрати CSV файл", command=self.load_csv)
        self.btn_select_file.pack(padx=10, pady=5, anchor=tk.W)

    def clear_window(self):
        for widget in self.history_frame.winfo_children():
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
        self.draw_results()

    def draw_results(self):
        frames = self.cd.get_frames(self.history_frame)
        for frame in frames:
            frame.pack()

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    app.run()
