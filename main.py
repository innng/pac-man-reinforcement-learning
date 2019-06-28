"""Implement the Q-Learning algorithm for Pac-Man game."""

from sys import argv
from decimal import Decimal

states = ["-", "0", "&"]
actions = ["U", "D", "L", "R"]

final_states = ["0", "&"]

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

if __name__ == "__main__":
    pass
