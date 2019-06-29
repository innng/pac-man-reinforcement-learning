
"""Implement the Q-Learning algorithm for Pac-Man game."""

import numpy as np
from sys import argv
from decimal import Decimal
from random import randint, random

states = ["-", "0", "&"]
actions = ["R", "L", "U", "D"]

final_states = ["0", "&"]
wall = "#"

rewards = {"-": Decimal("-1"), "0": Decimal("10"), "&": Decimal("-10")}
movement = {
    "R": (lambda x: x, lambda y: y + 1),
    "L": (lambda x: x, lambda y: y - 1),
    "U": (lambda x: x - 1, lambda y: y),
    "D": (lambda x: x + 1, lambda y: y),
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

    q_table = np.zeros((rows, cols, len(actions)), dtype=Decimal)


def write_value_file():
    """Write file with values from the q_table."""
    with open(value_file, "w") as fout:
        for r in range(rows):
            for c in range(cols):
                for a in range(len(actions)):
                    if q_table[r, c, a] != 0:
                        fout.write(f"{r},{c},{actions[a]},{q_table[r, c, a]:.3f}\n")


def write_policy_file():
    """Write the maze with the optimal policy."""
    global maze

    for r in range(rows):
        for c in range(cols):
            max_reward = max(q_table[r, c])

            if max_reward != 0:
                action = list(q_table[r, c]).index(max_reward)
                action = actions[action]

                maze[r, c] = action

    with open(policy_file, "w") as fout:
        for r in maze.tolist():
            fout.write("".join(r) + "\n")


def q_learning():
    """Run one episode of Q-Learning algorithm."""
    state = "&"

    while state in final_states or state == wall:
        x = randint(0, rows - 1)
        y = randint(0, cols - 1)

        state = maze[x, y]

    state = states.index(state)

    end_episode = False

    while not end_episode:
        if random() < exploration_factor:
            action = randint(0, len(actions) - 1)
        else:
            max_reward = max(q_table[x, y])
            action = list(q_table[x, y]).index(max_reward)

        dirx, diry = movement[actions[action]]
        new_x = dirx(x)
        new_y = diry(y)

        new_state = maze[new_x, new_y]

        if new_state == wall:
            reward = rewards["-"]

            q_table[x, y, action] += (
                learning_rate
                * (
                    reward
                    + discount_factor
                    * max(q_table[x, y])
                    - q_table[x, y, action]
                )
            )
        else:
            reward = rewards[new_state]

            new_state = states.index(new_state)

            q_table[x, y, action] += (
                learning_rate
                * (
                    reward
                    + discount_factor
                    * max(q_table[new_x, new_y])
                    - q_table[x, y, action]
                )
            )

            state = new_state
            x = new_x
            y = new_y

            if states[new_state] in final_states:
                end_episode = True


if __name__ == "__main__":
    read_input_file()
    create_q_table()

    graph_data = []

    for ep in range(episodes):
        q_learning()
        q = [x for sublist in q_table for subsublist in sublist for x in subsublist if x != 0]
        graph_data.append((ep, np.mean(q)))

    write_value_file()
    write_policy_file()
