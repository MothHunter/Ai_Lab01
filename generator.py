import numpy as np
import random


def generate_puzzle():
    random_generator_puzzle = np.random.choice(np.arange(9), size=(3, 3), replace=False)
    return random_generator_puzzle
