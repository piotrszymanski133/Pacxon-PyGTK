import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Dialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="O aplikacji", transient_for=parent, flags=0)
        self.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK)

        self.set_default_size(150, 100)

        label = Gtk.Label(label="Gra Pax-con - twórca Piotr Szymański")

        box = self.get_content_area()
        box.add(label)
        self.show_all()