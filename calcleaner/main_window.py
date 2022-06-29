from gi.repository import Gtk

from . import APPLICATION_NAME


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(
            self,
            application=app,
            title=APPLICATION_NAME,
            default_width=400,
            default_height=500,
            resizable=True,
        )
