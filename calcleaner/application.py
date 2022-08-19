from concurrent.futures import ThreadPoolExecutor

from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import GLib
import requests.exceptions
import caldav.lib.error

from . import APPLICATION_ID
from .main_window import MainWindow
from .account_edit_dialog import AccountEditDialog
from .accounts_manage_dialog import AccountsManageDialog
from . import caldav_helpers
from .about_dialog import AboutDialog
from .calendar_store import CalendarStore
from .accounts import Accounts
from .translation import gettext as _


class CalcleanerApplication(Gtk.Application):

    accounts = None
    calendar_store = None

    def __init__(self):
        Gtk.Application.__init__(
            self,
            application_id=APPLICATION_ID,
            flags=Gio.ApplicationFlags.HANDLES_OPEN,
        )
        self._stop_cleanning_requested = False
        self._main_window = None
        self.accounts = Accounts()
        self.calendar_store = CalendarStore()

    def do_startup(self):
        Gtk.Application.do_startup(self)
        self.accounts.load()

        # Action: app.add-account
        action = Gio.SimpleAction.new("add-account", None)
        action.connect("activate", lambda a, p: self.add_account())
        self.add_action(action)

        # Action: app.manage-accounts
        action = Gio.SimpleAction.new("manage-accounts", None)
        action.connect("activate", lambda a, p: self.manage_accounts())
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

        # Action: app.stop-cleanning
        action = Gio.SimpleAction.new("stop-cleanning", None)
        action.connect("activate", lambda a, p: self.stop_cleanning())
        self.add_action(action)

    def do_activate(self):
        if not self._main_window:
            self._main_window = MainWindow(self)
            if len(self.accounts.list()) > 0:
                self.fetch_calendars()

        self._main_window.show()
        self._main_window.present()

    def quit(self):
        self.stop_cleanning()
        Gtk.Application.quit(self)

    def about(self):
        about_dialog = AboutDialog(parent=self._main_window)
        about_dialog.run()
        about_dialog.destroy()

    def display_error(self, error):
        if hasattr(error, "account"):
            title = error.account
        else:
            title = _("An error occured...")

        if isinstance(error, requests.exceptions.SSLError):
            description = _(
                "Unable to connect to the server: the SSL certificate is invalid.\n\n"
                "🞄 Check that there is no error in the CalDAV server URL\n"
                "🞄 If you are using a self-signed certificate, disable the SSL "
                "verification in the parameters of the account"
            )
        elif isinstance(error, requests.exceptions.ConnectionError):
            description = _(
                "Unable to connect to the server.\n\n"
                "🞄 Check that there is no error in the CalDAV server URL\n"
                "🞄 Check that the server is currently available\n"
                "🞄 Check you are connected to the internet"
            )
        elif isinstance(error, caldav.lib.error.AuthorizationError):
            description = _(
                "You are not authorized to access this resource.\n\n"
                "🞄 Check your login and password\n"
                "🞄 Check you are allowed to access the server"
            )
        elif isinstance(error, caldav.lib.error.PropfindError):
            description = _(
                "Unable to read calendars.\n\n"
                "🞄 Check that there is no error in the CalDAV server URL"
            )
        else:
            description = _("Unknown error")

        self._main_window.set_error(
            title=title,
            description=description,
            detail=str(error),
        )
        self._main_window.set_state(self._main_window.STATE_ERROR)

    def add_account(self, update=True):
        dialog = AccountEditDialog(parent_window=self._main_window)
        account = dialog.run()

        if account:
            self.accounts.add(
                account["name"],
                url=account["url"],
                username=account["username"],
                password=account["password"],
            )
            if update:
                self.calendar_store.clear()
                self.fetch_calendars()

    def edit_account(self, account_name):
        orig_account = self.accounts.get(account_name)
        dialog = AccountEditDialog(
            url=orig_account["url"],
            username=orig_account["username"],
            password=orig_account["password"],
            parent_window=self._main_window,
        )
        new_account = dialog.run()

        if not new_account:
            return

        if new_account["name"] != account_name:
            self.accounts.remove(account_name)
            self.accounts.add(
                new_account["name"],
                url=new_account["url"],
                username=new_account["username"],
                password=new_account["password"],
            )
        else:
            self.accounts.update(
                account_name,
                url=new_account["url"],
                username=new_account["username"],
                password=new_account["password"],
            )

    def manage_accounts(self):
        dialog = AccountsManageDialog(self, parent_window=self._main_window)
        dialog.run()
        if len(self.accounts.list()) > 0:
            self.calendar_store.clear()
            self.fetch_calendars()
        else:
            self._main_window.set_state(self._main_window.STATE_INITIAL)

    def fetch_calendars(self):
        self._main_window.set_state(self._main_window.STATE_UPDATING)

        errors = []

        def _async_fetch_calendars():
            for account_name in self.accounts.list():
                account = self.accounts.get(account_name)
                try:
                    calendars = caldav_helpers.fetch_calendars(
                        account["url"],
                        account["username"],
                        account["password"],
                    )
                    for calendar in calendars:
                        iter_ = self.calendar_store.find_calendar_by_url(
                            calendar["url"]
                        )

                        if not iter_:
                            iter_ = self.calendar_store.append()

                        self.calendar_store.update(
                            iter_,
                            account_name=account_name,
                            calendar_url=calendar["url"],
                            calendar_name=calendar["name"],
                            calendar_color=calendar["color"],
                            event_count=calendar["event_count"],
                        )
                except Exception as error:
                    error.account = account_name
                    errors.append(error)
                    print(error)
                    raise error

        executor = ThreadPoolExecutor(max_workers=1)
        future = executor.submit(_async_fetch_calendars)

        def _async_wait_loop():
            if future.done():
                if errors:
                    self.display_error(errors[0])
                else:
                    self._main_window.set_state(self._main_window.STATE_CALENDAR_LIST)
                return
            GLib.timeout_add_seconds(0.1, _async_wait_loop)

        _async_wait_loop()

    def clean_calendars(self):
        self._main_window.set_state(self._main_window.STATE_CLEANING)

        self._stop_cleanning_requested = False
        max_age = int(self._main_window.max_age_spinbutton.get_value())
        keep_recurring_events = (
            self._main_window.keep_recurring_checkbutton.get_active()
        )

        for index in range(self.calendar_store.length):
            calendar = self.calendar_store.get(index)
            if calendar["clean_enabled"]:
                self.calendar_store.update(
                    index,
                    clean_progress=0,
                    clean_progress_text="-",
                )
            else:
                self.calendar_store.update(
                    index,
                    clean_progress=0,
                    clean_progress_text=_("Skipped"),
                )

        errors = []

        def _async_clean_calendars():
            try:
                for index in range(self.calendar_store.length):
                    if self._stop_cleanning_requested:
                        break

                    calendar = self.calendar_store.get(index)
                    account = self.accounts.get(calendar["account_name"])

                    if not calendar["clean_enabled"]:
                        continue

                    self.calendar_store.update(
                        index,
                        clean_progress=0,
                        clean_progress_text=_("Reading..."),
                    )

                    for cleaned_count, to_clean_count in caldav_helpers.clean_calendar(
                        calendar["calendar_url"],
                        account["username"],
                        account["password"],
                        max_age=max_age,
                        keep_recurring_events=keep_recurring_events,
                    ):
                        if self._stop_cleanning_requested:
                            break
                        if to_clean_count > 0:
                            progress = cleaned_count / to_clean_count * 100
                        else:
                            progress = 100

                        self.calendar_store.update(
                            index,
                            clean_progress=progress,
                            clean_progress_text="%i / %i"
                            % (cleaned_count, to_clean_count),
                        )
            except Exception as error:
                error.account = calendar["account_name"]
                errors.append(error)
                print(error)
                raise error

        executor = ThreadPoolExecutor(max_workers=1)
        future = executor.submit(_async_clean_calendars)

        def _async_wait_loop():
            if future.done():
                if errors:
                    self.display_error(errors[0])
                else:
                    self.fetch_calendars()
                return
            GLib.timeout_add_seconds(0.1, _async_wait_loop)

        _async_wait_loop()

    def stop_cleanning(self):
        self._stop_cleanning_requested = True
