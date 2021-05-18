import random

all_clues_list = ["red", "blue", "green", "yellow"]

phantom_clues_dict = {
  "phantom_1": ["red", "blue", "green"],
  "phantom_2": ["red", "blue", "yellow"]
}


class CluesHandler:
    def __init__(self):
        self.current_phantom = random.choice(list(phantom_clues_dict.values()))
        print(self.current_phantom)

    def add_player(self, player):
        sda