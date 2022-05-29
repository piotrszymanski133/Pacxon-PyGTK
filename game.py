from level import Level


class Game:
    def __init__(self, window):
        self.score = 0
        self.level_changed = False
        self.previous_level = 0
        self.levels = []
        self.levels.append(Level(0, 2, 0, window))
        self.levels.append(Level(1, 1, 0, window))
        self.levels.append(Level(2, 3, 1, window))
        self.actual_level = self.levels[0]
        self.actual_level_number = 1

    def game_iteration(self):
        if self.actual_level.map.filled_blocks_counter / self.actual_level.map.blocks_number >= 0.8:
            self.actual_level.map.clean()
            self.actual_level.pacman.move_to(0, 25)
            self.level_changed = True
            self.previous_level = self.actual_level_number
            if self.actual_level == self.levels[2]:
                self.actual_level = self.levels[0]
                self.actual_level_number = 1
            else:
                self.actual_level_number += 1
                self.actual_level = self.levels[self.actual_level_number - 1]
        self.actual_level.game_iteration()
