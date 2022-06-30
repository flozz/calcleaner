from gi.repository import Gtk
from gi.repository import Gio

from . import APPLICATION_ID
from .main_window import MainWindow
from .caldav_dialog import CaldavDialog


class CalcleanerApplication(Gtk.Application):

    accounts = {}

    def __init__(self):
        Gtk.Application.__init__(
            self,
            application_id=APPLICATION_ID,
            flags=Gio.ApplicationFlags.HANDLES_OPEN,
        )
        self._main_window = None

    def do_startup(self):
        Gtk.Application.do_startup(self)

        # Action: app.add-caldav
        action = Gio.SimpleAction.new("add-caldav", None)
        action.connect("activate", lambda a, p: self.add_caldav())
        self.add_action(action)

    def do_activate(self):
        if not self._main_window:
            self._main_window = MainWindow(self)

        self._main_window.show()
        self._main_window.present()

    def add_caldav(self):
        caldav_dialog = CaldavDialog(parent_window=self._main_window)

        # XXX DEBUG ===============================================================
        caldav_dialog._url_entry.set_text("http://localhost:8080/remote.php/dav")
        caldav_dialog._username_entry.set_text("admin")
        caldav_dialog._password_entry.set_text("password")
        # XXX DEBUG ===============================================================

        caldav_account = caldav_dialog.run()

        if caldav_account:
            self.accounts[caldav_account["url"]] = {
                "username": caldav_account["username"],
                "password": caldav_account["password"],
                "calendars": {
                    # "url": {"name": name, "color": color, "events_count": 0}
                },
            }
            self.fetch_calendars()

    def fetch_calendars(self):
        self._main_window.set_state(self._main_window.STATE_UPDATING)
        # TODO
        self._main_window.set_state(self._main_window.STATE_CALENDAR_LIST)
