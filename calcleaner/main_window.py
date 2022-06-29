from gi.repository import Gtk

from . import APPLICATION_NAME
from . import data_helpers


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(
            self,
            application=app,
            title=APPLICATION_NAME,
            default_width=400,
            default_height=300,
            resizable=True,
        )

        self._builder = Gtk.Builder()
        self._builder.add_from_file(data_helpers.find_data_path("ui/main-window.glade"))
        self._builder.connect_signals(self)

        content = self._builder.get_object("main-window-content")
        self.add(content)
