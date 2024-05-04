import csv
import random

from _consts import ALTERNATIVES


def generate_random_row():
    return random.sample(ALTERNATIVES, len(ALTERNATIVES))


def write_csv(filename, rows):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in rows:
            writer.writerow(row)


if __name__ == "__main__":
    num_rows = 100
    rows = [generate_random_row() for _ in range(num_rows)]
    write_csv('random_vote.csv', rows)
