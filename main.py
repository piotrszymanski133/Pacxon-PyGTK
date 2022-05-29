import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from window import Window
import sys

sys.setrecursionlimit(1500)
window = Window()
window.show()
window.connect("destroy", Gtk.main_quit)
Gtk.main()