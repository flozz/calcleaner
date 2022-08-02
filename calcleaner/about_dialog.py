from gi.repository import Gtk
from gi.repository import GdkPixbuf

from . import APPLICATION_NAME
from . import VERSION
from . import data_helpers
from .translation import gettext as _


class AboutDialog(Gtk.AboutDialog):
    def __init__(self, parent=None):
        Gtk.AboutDialog.__init__(
            self,
            parent=parent,
            program_name=APPLICATION_NAME,
            comments=_(
                "A simple graphical tool to purge old events from CalDAV calendars"
            ),
            version=VERSION,
            copyright="Copyright (c) 2022 Fabien LOISON",
            website_label="github.com/flozz/calcleaner",
            website="https://github.com/flozz/calcleaner",
            license_type=Gtk.License.GPL_3_0,
        )

        logo = GdkPixbuf.Pixbuf.new_from_file(
            data_helpers.find_data_path("images/calcleaner_128.png")
        )
        self.set_logo(logo)

        self.set_translator_credits(_("translator-credits"))
