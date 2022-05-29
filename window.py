import gi

from block_type import BlockType

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject, GLib
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, BLOCK_SIZE
from dialog import Dialog
from game import Game


class Window(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.box = Gtk.Fixed()
        self.drawing_area = None
        self.restarted = False
        self.timer = None
        self.level_label = None
        self.level_score_label = None
        self.score_label = None
        self.lives_label = None
        self.button = None
        self.picture = None
        self.blocks = []
        self.game = None
        self.add(self.box)
        self.connect("key_press_event", self.__on_key_pressed)
        self.connect("key_release_event", self.__on_key_release)
        self.connect("delete-event", Gtk.main_quit)

        self.show_start_screen()
        self.show_all()

    def show_start_screen(self):
        self.__create_start_screen_background()
        self.__create_start_button()
        self.__set_window_properties()
        self.__create_menu_bar()
        self.show()

    def show_game_screen(self):
        if self.button is None:
            self.__remove_labels()
        if self.button is not None:
            self.__remove_start_screen()
        self.init_draw()
        self.__show_characters()
        self.__create_score_label()

    def init_draw(self):
        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.set_size_request(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.drawing_area.connect("draw", self.draw_map)
        self.drawing_area.queue_draw()
        self.box.put(self.drawing_area, 0, 0)
        self.show_all()

    def draw_map(self, wdg, context):
        context.set_line_width(2)
        for block_row in self.game.actual_level.map.blocks:
            for block in block_row:
                context.set_source_rgb(0.0, 0.0, 0.0)
                context.rectangle(block.x, block.y, BLOCK_SIZE, BLOCK_SIZE)
                context.stroke_preserve()
                if block.type == BlockType.UNBREAKABLE_WALL:
                    context.set_source_rgb(0.0, 0.0, 0.7)
                elif block.type == BlockType.EMPTY:
                    context.set_source_rgb(0.9, 0.9, 0.9)
                elif block.type == BlockType.BREAKABLE_WALL:
                    context.set_source_rgb(0.0, 0.0, 1.0)
                context.fill()
        self.__update_label(self.level_label, 'Poziom  ' + str(self.game.actual_level_number))
        self.__update_label(self.score_label, "Punkty: " + str(self.game.actual_level.map.filled_blocks_counter))
        self.__update_label(self.lives_label, "Zycia: " + str(self.game.actual_level.pacman.lives))
        self.__update_label(self.level_score_label, "Wynik:" +
                                str(int(self.game.actual_level.map.filled_blocks_counter
                                        / self.game.actual_level.map.blocks_number * 100)) + "/80%")
        return True

    def __start_game(self, option):
        self.__clean()
        if self.game is not None:
            self.restarted = True

        self.game = Game(self)
        self.show_game_screen()
        self.show_all()
        GLib.timeout_add(2, self.__game_iteration)
        loop = GLib.MainLoop()
        loop.run()

    def __game_iteration(self):
        if self.restarted:
            self.restarted = False
            return False
        if self.game.level_changed:
            if self.game.actual_level_number > 3:
                self.close()
            self.box.remove(self.game.levels[self.game.previous_level - 1].pacman.picture)
            for ghost in self.game.levels[self.game.previous_level - 1].ghosts:
                self.box.remove(ghost.picture)
            self.game.level_changed = False
            self.__show_characters()
        for ghost in self.game.actual_level.ghosts:
            self.box.move(ghost.picture, ghost.x, ghost.y)
        pacman = self.game.actual_level.pacman
        self.box.move(pacman.picture, pacman.x, pacman.y)
        self.game.game_iteration()
        return True

    def __create_menu_bar(self):
        menu_bar = Gtk.MenuBar()
        game_m = Gtk.Menu()
        info_m = Gtk.Menu()
        game_menu = Gtk.MenuItem("Gra")
        info_menu = Gtk.MenuItem("Informacje")
        start = Gtk.MenuItem("Start")
        quit = Gtk.MenuItem("Wyjście")
        about_application = Gtk.MenuItem("O aplikacji")
        game_menu.set_submenu(game_m)
        info_menu.set_submenu(info_m)
        game_m.append(start)
        game_m.append(quit)
        info_m.append(about_application)
        menu_bar.append(game_menu)
        menu_bar.append(info_menu)
        start.connect('activate', self.__start_game)

        quit.connect('activate', Gtk.main_quit)
        menu_bar.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse('#FFFFFF'))
        vbox = Gtk.VBox(False, 2)
        vbox.pack_start(menu_bar, False, False, 0)
        self.box.put(vbox, 0, 0)
        about_application.connect('activate', self.show_info_about_application)

    def show_info_about_application(self, ddd):
        mbox = Dialog(self)
        mbox.run()
        mbox.destroy()

    def __create_start_button(self):
        self.button = Gtk.Button.new_with_label("START")
        self.button.set_size_request(400, 100)
        self.button.connect("clicked", self.__start_game)
        self.grid = Gtk.Grid(valign=Gtk.Align.CENTER, halign=Gtk.Align.CENTER)
        self.grid.add(self.button)
        self.box.put(self.grid, WINDOW_WIDTH / 2 - 200, WINDOW_HEIGHT / 2 - 50)

    def __create_start_screen_background(self):
        self.picture = Gtk.Image.new_from_file('static/pac-xon-deluxe.jpg')
        self.box.put(self.picture, 0, 25)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

    def __create_score_label(self):
        self.level_label = Gtk.Label()
        self.level_label.set_text('Poziom  ' + str(self.game.actual_level_number))
        self.box.put(self.level_label, 0, WINDOW_HEIGHT - 15)

        self.score_label = Gtk.Label()
        self.score_label.set_text("Punkty: " + str(self.game.score))
        self.box.put(self.score_label, 130, WINDOW_HEIGHT - 15)

        self.level_score_label = Gtk.Label()
        self.level_score_label.set_text("Wynik: 0/80%")
        self.box.put(self.level_score_label, 280, WINDOW_HEIGHT - 15)

        self.lives_label = Gtk.Label()
        self.lives_label.set_text("Zycia: " + str(self.game.actual_level.pacman.lives))
        self.box.put(self.lives_label, 450, WINDOW_HEIGHT - 15)

    def __update_label(self, label, text):
        label.set_text(text)

    def __set_window_properties(self):
        self.set_size_request(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.set_title("Pacxon")

    def __remove_start_screen(self):
        self.box.remove(self.picture)
        self.box.remove(self.grid)
        self.grid.remove(self.button)
        self.button = None

    def __show_characters(self):
        for ghost in self.game.actual_level.ghosts:
            self.box.put(ghost.picture, ghost.x, ghost.y)

        pacman = self.game.actual_level.pacman
        self.box.put(pacman.picture, pacman.x, pacman.y)
        self.show_all()

    def __remove_labels(self):
        self.box.remove(self.level_label)
        self.box.remove(self.lives_label)
        self.box.remove(self.level_score_label)
        self.box.remove(self.score_label)

    def __clean(self):
        if self.game is not None:
            self.box.remove(self.game.actual_level.pacman.picture)
            for ghost in self.game.actual_level.ghosts:
                self.box.remove(ghost.picture)

    def __on_key_pressed(self, wdg, event):
        if self.game is not None and not self.game.actual_level.game_over:
            keyname = Gdk.keyval_name(event.keyval)
            pacman = self.game.actual_level.pacman
            self.box.remove(pacman.picture)
            if keyname == "d":
                pacman.start_move(0, 1)
            if keyname == "a":
                pacman.start_move(0, -1)
            if keyname == "w":
                pacman.start_move(1, -1)
            if keyname == "s":
                pacman.start_move(1, 1)
            self.box.put(pacman.picture, pacman.x, pacman.y)
            self.show_all()

    def __on_key_release(self, wdg, event):
        if self.game is not None:
            self.game.actual_level.pacman.end_move()