from concurrent.futures import ThreadPoolExecutor

from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import GLib
import requests.exceptions
import caldav.lib.error

from . import APPLICATION_ID
from .main_window import MainWindow
from .caldav_dialog import CaldavDialog
from . import caldav_helpers
from .about_dialog import AboutDialog
from .calendar_store import CalendarStore


class CalcleanerApplication(Gtk.Application):

    accounts = {}
    calendar_store = None

    def __init__(self):
        Gtk.Application.__init__(
            self,
            application_id=APPLICATION_ID,
            flags=Gio.ApplicationFlags.HANDLES_OPEN,
        )
        self._main_window = None
        self.calendar_store = CalendarStore()

    def do_startup(self):
        Gtk.Application.do_startup(self)

        # Action: app.add-caldav
        action = Gio.SimpleAction.new("add-caldav", None)
        action.connect("activate", lambda a, p: self.add_caldav())
        self.add_action(action)

        # Action: app.refresh
        action = Gio.SimpleAction.new("refresh", None)
        action.connect("activate", lambda a, p: self.fetch_calendars())
        self.add_action(action)

        # Action: app.clean
        action = Gio.SimpleAction.new("clean", None)
        action.connect("activate", lambda a, p: self.clean_calendars())
        self.add_action(action)

        # Action: app.about
        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", lambda a, p: self.about())
        self.add_action(action)

        # Action: app.quit
        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", lambda a, p: self.quit())
        self.add_action(action)
        self.set_accels_for_action("app.quit", ["<Ctrl>Q", "<Ctrl>W"])

    def do_activate(self):
        if not self._main_window:
            self._main_window = MainWindow(self)

        self._main_window.show()
        self._main_window.present()

    def quit(self):
        Gtk.Application.quit(self)

    def about(self):
        about_dialog = AboutDialog(parent=self._main_window)
        about_dialog.run()
        about_dialog.destroy()

    def add_caldav(self):
        caldav_dialog = CaldavDialog(parent_window=self._main_window)

        # XXX DEBUG ===============================================================
        caldav_dialog._url_entry.set_text("http://localhost:8080/remote.php/dav")
        caldav_dialog._username_entry.set_text("admin")
        caldav_dialog._password_entry.set_text("password")
        # XXX DEBUG ===============================================================

        account = caldav_dialog.run()

        if account:
            self.accounts[account["name"]] = {
                "url": account["url"],
                "username": account["username"],
                "password": account["password"],
            }
            self.fetch_calendars()

    def fetch_calendars(self):
        self._main_window.set_state(self._main_window.STATE_UPDATING)

        for account in self.accounts:
            self.accounts[account]["calendars"] = {}

        errors = []

        def _async_fetch_calendars(accounts):
            for account_name, account in accounts.items():
                try:
                    calendars = caldav_helpers.fetch_calendars(
                        account["url"],
                        account["username"],
                        account["password"],
                    )
                    for calendar in calendars:
                        self.calendar_store.append(
                            account_name=account_name,
                            calendar_url=calendar["url"],
                            calendar_name=calendar["name"],
                            calendar_color=calendar["color"],
                            event_count=calendar["event_count"],
                        )
                        # TODO update
                except Exception as error:
                    error.account = account_name
                    errors.append(error)
                    print(error)
                    raise error

        executor = ThreadPoolExecutor(max_workers=1)
        future = executor.submit(_async_fetch_calendars, self.accounts)

        def _async_wait_loop():
            if future.done():
                if errors:
                    error = errors[0]

                    if hasattr(error, "account"):
                        title = error.account
                    else:
                        title = "An error occured..."

                    if isinstance(error, requests.exceptions.ConnectionError):
                        # fmt: off
                        description = "Unable to connect to the server.\n\n"
                        description += "🞄 Check that there is no error in the CalDAV server URL\n"
                        description += "🞄 Check that the server is currently available\n"
                        description += "🞄 Check you are connected to the internet"
                        # fmt: on
                    elif isinstance(error, caldav.lib.error.AuthorizationError):
                        # fmt: off
                        description = "You are not authorized to access this resource.\n\n"
                        description += "🞄 Check your login and password\n"
                        description += "🞄 Check you are allowed to access the server"
                        # fmt: on
                    elif isinstance(error, caldav.lib.error.PropfindError):
                        # fmt: off
                        description = "Unable to read calendars.\n\n"
                        description += "🞄 Check that there is no error in the CalDAV server URL"
                        # fmt: on
                    else:
                        description = "Unknown error"

                    self._main_window.set_error(
                        title=title,
                        description=description,
                        detail=str(errors[0]),
                    )
                    self._main_window.set_state(self._main_window.STATE_ERROR)
                else:
                    self._main_window.set_state(self._main_window.STATE_CALENDAR_LIST)
                return
            GLib.timeout_add_seconds(0.1, _async_wait_loop)

        _async_wait_loop()

    def clean_calendars(self):
        self._main_window.set_state(self._main_window.STATE_CLEANING)
        # TODO
