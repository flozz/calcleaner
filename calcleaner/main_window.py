from gi.repository import Gtk

from . import APPLICATION_NAME
from . import data_helpers


class MainWindow(Gtk.ApplicationWindow):

    STATE_INITIAL = "state-initial"
    STATE_UPDATING = "state-updating"
    STATE_CALENDAR_LIST = "state-calendar-list"

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

        self.set_state(self.STATE_INITIAL)

    def set_state(self, state):
        initial_root = self._builder.get_object("state-initial")
        updating_root = self._builder.get_object("state-updating")
        calendar_list_root = self._builder.get_object("state-calendar-list")

        initial_root.set_visible(state == self.STATE_INITIAL)
        updating_root.set_visible(state == self.STATE_UPDATING)
        calendar_list_root.set_visible(state == self.STATE_CALENDAR_LIST)
