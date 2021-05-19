import random

all_clues_list = ["red", "blue", "green", "yellow", "purple"]

phantom_clues_dict = {
  "phantom_1": ["red", "blue", "green"],
  "phantom_2": ["red", "blue", "yellow"],
  "phantom_3": ["red", "yellow", "green"],
  "phantom_4": ["yellow", "blue", "green"],
  "phantom_5": ["purple", "blue", "green"],
  "phantom_6": ["purple", "blue", "red"],
  "phantom_7": ["purple", "red", "yellow"]
}

group_clues_dict = {
  1: [1, 2, 3],
  2: [1, 2, 3],
  3: [1, 2],
  4: [1, 2, 3]
}


class CluesHandler:
    def __init__(self):
        self.current_phantom = random.choice(list(phantom_clues_dict.keys()))
        self.clues_holder = self.set_clues_spawner()

    def set_clues_spawner(self):
        clues_holder = {}
        discriminator = random.choice(list(group_clues_dict.keys()))
        for clue in group_clues_dict:
            if discriminator == clue:
                continue
            clues_holder[clue] = random.choice(group_clues_dict[clue])
        return clues_holder

    def get_phantom_type(self):
        return self.current_phantom

    def get_clues_holder(self):
        return self.clues_holder