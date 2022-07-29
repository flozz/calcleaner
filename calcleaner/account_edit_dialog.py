import re

from gi.repository import Gtk

from . import data_helpers
from . import caldav_helpers


class AccountEditDialog(object):
    def __init__(self, url="", username="", password="", parent_window=None):
        self._response = None

        self._builder = Gtk.Builder()
        self._builder.add_from_file(
            data_helpers.find_data_path("ui/account-edit-dialog.glade")
        )
        self._builder.connect_signals(self)

        self._dialog = self._builder.get_object("account-edit-dialog")
        self._dialog.set_transient_for(parent_window)

        self._url_entry = self._builder.get_object("url-entry")
        self._url_entry.set_text(url)
        self._username_entry = self._builder.get_object("username-entry")
        self._username_entry.set_text(username)
        self._password_entry = self._builder.get_object("password-entry")
        self._password_entry.set_text(password)
        self._connect_button = self._builder.get_object("connect-button")

        self._validate_inputs()

    def run(self):
        self._dialog.run()
        return self._response

    def _validate_inputs(self, *args):
        inputs_ok = True

        if not re.match(r"https?://.+", self._url_entry.get_text()):
            inputs_ok = False

        if not self._username_entry.get_text():
            inputs_ok = False

        if not self._password_entry.get_text():
            inputs_ok = False

        self._connect_button.set_sensitive(inputs_ok)

    def _on_cancel(self, *args):
        self._dialog.destroy()

    def _on_validate(self, *args):
        self._response = {
            "name": caldav_helpers.readable_account_url(
                self._url_entry.get_text(),
                self._username_entry.get_text(),
            ),
            "url": self._url_entry.get_text(),
            "username": self._username_entry.get_text(),
            "password": self._password_entry.get_text(),
        }
        self._dialog.destroy()
