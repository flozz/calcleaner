from gi.repository import Gtk
from gi.repository import Gio

from . import APPLICATION_ID
from .main_window import MainWindow


class CalcleanerApplication(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(
            self,
            application_id=APPLICATION_ID,
            flags=Gio.ApplicationFlags.HANDLES_OPEN,
        )
        self._main_window = None

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def do_activate(self):
        if not self._main_window:
            self._main_window = MainWindow(self)
        self._main_window.show()
        self._main_window.present()
