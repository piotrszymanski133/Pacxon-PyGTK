import copy
from constants import BLOCK_SIZE
from block import Block
from block_type import BlockType


class Map:
    def __init__(self, window):
        self.blocks = []
        self.window = window
        self.filled_blocks_counter = 0
        self.blocks_number = 23 * 40
        for i in range(42):
            block_row = []
            for j in range(1, 26):
                if i == 0 or j == 1 or i == 41 or j == 25:
                    block_row.append(Block(i * BLOCK_SIZE, j * BLOCK_SIZE, BlockType.UNBREAKABLE_WALL))
                else:
                    block_row.append(Block(i * BLOCK_SIZE, j * BLOCK_SIZE, BlockType.EMPTY))
            self.blocks.append(block_row)

    def get_block(self, x, y) -> Block:
        if x < 0 or y < 25:
            return Block(-1, -1, BlockType.NO_BLOCK)
        try:
            x_index = x / BLOCK_SIZE
            y_index = (y - 25) / BLOCK_SIZE
            return self.blocks[int(x_index)][int(y_index)]
        except IndexError:
            return Block(-1, -1, BlockType.NO_BLOCK)

    def change_block_type(self, x, y, block_type):
        x_index = x / BLOCK_SIZE
        y_index = (y - BLOCK_SIZE) / BLOCK_SIZE
        self.blocks[int(x_index)][int(y_index)].change_type(block_type)

    def get_temporary_blocks(self):
        tmp_blocks = []
        for block_row in self.blocks:
            for block in block_row:
                if block.type == BlockType.TEMPORARY_WALL:
                    tmp_blocks.append(block)
        return tmp_blocks

    def try_to_fill_empty_spaces(self, start_point_x, start_point_y):
        start_block_left = self.get_block(start_point_x - BLOCK_SIZE, start_point_y)
        filled_maps = []
        if start_block_left.type == BlockType.EMPTY:
            m = copy.copy(self)
            m.blocks = copy.deepcopy(self.blocks)
            filled_maps.append(self.__fill_space(start_block_left.x, start_block_left.y, m))

        start_block_right = self.get_block(start_point_x + BLOCK_SIZE, start_point_y)
        if start_block_right.type == BlockType.EMPTY:
            m = copy.copy(self)
            m.blocks = copy.deepcopy(self.blocks)
            filled_maps.append(self.__fill_space(start_block_right.x, start_block_right.y, m))

        start_block_up = self.get_block(start_point_x, start_point_y - BLOCK_SIZE)
        if start_block_up.type == BlockType.EMPTY:
            m = copy.copy(self)
            m.blocks = copy.deepcopy(self.blocks)
            filled_maps.append(self.__fill_space(start_block_up.x, start_block_up.y, m))

        start_block_down = self.get_block(start_point_x, start_point_y + BLOCK_SIZE)
        if start_block_down.type == BlockType.EMPTY:
            m = copy.copy(self)
            m.blocks = copy.deepcopy(self.blocks)
            filled_maps.append(self.__fill_space(start_block_down.x, start_block_down.y, m))

        return filled_maps

    def merge_maps(self, another_map):
        for i in range(len(self.blocks)):
            for j in range(len(self.blocks[i])):
                if another_map.blocks[i][j].type == BlockType.BREAKABLE_WALL and self.blocks[i][j].type != BlockType.BREAKABLE_WALL:
                    self.blocks[i][j].change_type(BlockType.BREAKABLE_WALL)

    def update_counter(self):
        self.filled_blocks_counter = 0
        for block_row in self.blocks:
            for block in block_row:
                if block.type == BlockType.BREAKABLE_WALL:
                    self.filled_blocks_counter += 1

    def remove_tmp_blocks(self):
        blocks = self.get_temporary_blocks()
        for block in blocks:
            block.change_type(BlockType.EMPTY)

    def __fill_space(self, x, y, map):
        if map.get_block(x, y).type == BlockType.EMPTY:
            map.change_block_type(x, y, BlockType.BREAKABLE_WALL)
            self.__fill_space(x - BLOCK_SIZE, y, map)
            self.__fill_space(x + BLOCK_SIZE, y, map)
            self.__fill_space(x, y - BLOCK_SIZE, map)
            self.__fill_space(x, y + BLOCK_SIZE, map)
        return map

    def clean(self):
        self.filled_blocks_counter = 0
        for block_row in self.blocks:
            for block in block_row:
                if block.type != BlockType.UNBREAKABLE_WALL:
                    block.change_type(BlockType.EMPTY)

    def change_blocks_type(self, blocks, block_type):
        for block in blocks:
            x_index = block.x / BLOCK_SIZE
            y_index = (block.y - BLOCK_SIZE) / BLOCK_SIZE
            self.blocks[int(x_index)][int(y_index)].change_type(block_type)
