from ghost import Ghost
from ghost_type import GhostType
from pacman import Pacman
from map import Map
from block_type import BlockType
from constants import BLOCK_SIZE


class Level:
    def __init__(self, red_ghosts, purple_ghosts, orange_ghosts, window):
        self.ghosts = []
        self.game_over = False
        self.window = window
        self.pacman = Pacman(window)
        self.map = Map(window)
        for i in range(purple_ghosts):
            self.ghosts.append(Ghost(GhostType.PURPLE, window))
        for i in range(red_ghosts):
            self.ghosts.append(Ghost(GhostType.RED, window))
        for i in range(orange_ghosts):
            self.ghosts.append(Ghost(GhostType.ORANGE, window))

    def game_iteration(self):
        self.__move_ghosts()
        pacman_block = self.map.get_block(self.pacman.x, self.pacman.y)
        if pacman_block.type == BlockType.EMPTY:
            self.map.change_block_type(self.pacman.x, self.pacman.y, BlockType.TEMPORARY_WALL)
        elif pacman_block.type == BlockType.UNBREAKABLE_WALL or pacman_block.type == BlockType.BREAKABLE_WALL:
            tmp_blocks = self.map.get_temporary_blocks()
            if len(tmp_blocks) > 0:
                i = 0
                while i < len(tmp_blocks):
                    self.map.change_blocks_type(tmp_blocks, BlockType.BREAKABLE_WALL)
                    filled_maps = self.map.try_to_fill_empty_spaces(tmp_blocks[i].x, tmp_blocks[i].y)
                    for map in filled_maps:
                        can_be_used = True
                        for ghost in self.ghosts:
                            if ghost.type != GhostType.ORANGE and map.get_block(ghost.x, ghost.y).type == \
                                    BlockType.BREAKABLE_WALL:
                                can_be_used = False

                        if can_be_used:
                            self.map.merge_maps(map)
                    i += 4

        self.pacman.move_iteration()
        self.map.update_counter()

    def __kill_pacman(self):
        self.pacman.lives -= 1
        if self.pacman.lives <= 0:
            self.__game_over()
        else:
            self.pacman.move_to(0, 25)
            self.map.remove_tmp_blocks()

    def __move_ghosts(self):
        for ghost in self.ghosts:
            if ghost.x_velocity > 0:
                next_block_in_width = self.map.get_block(ghost.x + BLOCK_SIZE + ghost.x_velocity, ghost.y)
            else:
                next_block_in_width = self.map.get_block(ghost.x + ghost.x_velocity, ghost.y)
            if ghost.y_velocity < 0:
                next_block_in_height = self.map.get_block(ghost.x, ghost.y + ghost.y_velocity)
            else:
                next_block_in_height = self.map.get_block(ghost.x, ghost.y + BLOCK_SIZE + ghost.y_velocity)

            if ghost.type == GhostType.PURPLE:
                if next_block_in_width.type == BlockType.UNBREAKABLE_WALL or next_block_in_width.type == BlockType.BREAKABLE_WALL:
                    ghost.x_velocity = -ghost.x_velocity
                if next_block_in_height.type == BlockType.UNBREAKABLE_WALL or next_block_in_height.type == BlockType.BREAKABLE_WALL:
                    ghost.y_velocity = -ghost.y_velocity

                if next_block_in_width.type == BlockType.TEMPORARY_WALL or next_block_in_height.type == BlockType.TEMPORARY_WALL:
                    self.__kill_pacman()

            elif ghost.type == GhostType.RED:
                if next_block_in_width.type == BlockType.UNBREAKABLE_WALL or next_block_in_width.type == BlockType.BREAKABLE_WALL:
                    ghost.x_velocity = -ghost.x_velocity
                    if next_block_in_width.type == BlockType.BREAKABLE_WALL:
                        self.map.change_block_type(next_block_in_width.x, next_block_in_width.y, BlockType.EMPTY)
                if next_block_in_height.type == BlockType.UNBREAKABLE_WALL or next_block_in_height.type == BlockType.BREAKABLE_WALL:
                    ghost.y_velocity = -ghost.y_velocity
                    if next_block_in_height.type == BlockType.BREAKABLE_WALL:
                        self.map.change_block_type(next_block_in_height.x, next_block_in_height.y, BlockType.EMPTY)

                if next_block_in_width.type == BlockType.TEMPORARY_WALL or next_block_in_height.type == BlockType.TEMPORARY_WALL:
                    self.__kill_pacman()

            else:
                if next_block_in_width.type == BlockType.EMPTY or next_block_in_width.type == BlockType.NO_BLOCK:
                    ghost.x_velocity = -ghost.x_velocity
                if next_block_in_height.type == BlockType.EMPTY or next_block_in_height.type == BlockType.NO_BLOCK:
                    ghost.y_velocity = -ghost.y_velocity
                if next_block_in_width.type == BlockType.TEMPORARY_WALL or\
                    next_block_in_height.type == BlockType.TEMPORARY_WALL or\
                    self.map.get_block(ghost.x, ghost.y) == self.map.get_block(self.pacman.x, self.pacman.y):
                    self.__kill_pacman()
            ghost.move()

    def __game_over(self):
        self.game_over = True
