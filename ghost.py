import random
from ghost_type import GhostType
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, BLOCK_SIZE
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Ghost:
    def __init__(self, ghost_type, window):
        self.type = ghost_type
        self.window = window
        if ghost_type == GhostType.ORANGE:
            self.x = random.randint(WINDOW_WIDTH - BLOCK_SIZE, WINDOW_WIDTH)
            self.y = random.randint(WINDOW_HEIGHT - 3 * BLOCK_SIZE, WINDOW_HEIGHT - 2 * BLOCK_SIZE)
        else:
            self.x = random.randint(BLOCK_SIZE, int(WINDOW_WIDTH - 3 * BLOCK_SIZE))
            self.y = random.randint(BLOCK_SIZE * 2, int(WINDOW_HEIGHT - 3 * BLOCK_SIZE))

        if random.randint(0, 1) == 1:
            self.x_velocity = 2
        else:
            self.x_velocity = -2
        if random.randint(0, 1) == 1:
            self.y_velocity = 2
        else:
            self.y_velocity = -2

        if ghost_type == GhostType.PURPLE:
            picture_path = 'static/purple-ghost.png'
        elif ghost_type == GhostType.RED:
            picture_path = 'static/red-ghost.png'
        else:
            picture_path = 'static/orange-ghost.png'

        self.picture = Gtk.Image.new_from_file(picture_path)

    def move(self):
        self.x += self.x_velocity
        self.y += self.y_velocity