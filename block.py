

class Block:
    def __init__(self, x, y, block_type):
        self.x = x
        self.y = y
        self.type = block_type

    def change_type(self, type):
        self.type = type
