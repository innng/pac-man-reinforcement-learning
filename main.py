
"""Implement the Q-Learning algorithm for Pac-Man game."""

import numpy as np
from sys import argv
from decimal import Decimal

states = ["-", "0", "&"]
actions = ["U", "D", "L", "R"]

final_states = ["0", "&"]
wall = "#"

rewards = {"-": -1, "0": 10, "&": -10}
movement = {
    "U": (lambda x: x - 1, lambda y: y),
    "D": (lambda x: x + 1, lambda y: y),
    "L": (lambda x: x, lambda y: y - 1),
    "R": (lambda x: x, lambda y: y + 1)
}

discount_factor = Decimal("0.9")

rows = 0
cols = 0

maze = None
q_table = None

filename = argv[1]
learning_rate = Decimal(argv[2])
exploration_factor = Decimal(argv[3])
episodes = int(argv[4])

value_file = "q.txt"
policy_file = "pi.txt"


def read_input_file():
    """Get the number of rows and cols and the maze from input file."""
    global rows
    global cols
    global maze

    with open(filename, "r") as fout:
        a = fout.readline()
        rows, cols = tuple(a.split())
        rows = int(rows)
        cols = int(cols)

        maze = fout.readlines()
        maze = [list(r.strip(" \n")) for r in maze]
        maze = np.matrix(maze, dtype=str)


def create_q_table():
    """Create a table for states x actions values."""
    global q_table

    q_table = np.zeros((len(states), len(actions)), dtype=Decimal)


if __name__ == "__main__":
    read_input_file()
    create_q_table()
