from gi.repository import Gtk
from gi.repository import GdkPixbuf

from . import APPLICATION_NAME
from . import data_helpers


class MainWindow(Gtk.ApplicationWindow):

    STATE_INITIAL = "state-initial"
    STATE_UPDATING = "state-updating"
    STATE_ERROR = "state-error"
    STATE_CALENDAR_LIST = "state-calendar-list"
    STATE_CLEANING = "state-cleaning"

    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(
            self,
            application=app,
            title=APPLICATION_NAME,
            default_width=400,
            default_height=350,
            resizable=True,
        )

        self._builder = Gtk.Builder()
        self._builder.add_from_file(data_helpers.find_data_path("ui/main-window.glade"))
        self._builder.connect_signals(self)

        content = self._builder.get_object("main-window-content")
        self.add(content)

        self._header = self._builder.get_object("main-window-header")
        self.set_titlebar(self._header)

        initial_logo = self._builder.get_object("initial-logo")
        initial_logo.set_from_pixbuf(
            GdkPixbuf.Pixbuf.new_from_file(
                data_helpers.find_data_path("images/calcleaner_128.png")
            )
        )

        self._column_checkbox = None
        self._column_progress = None
        self._initialize_treeview()

        self.set_state(self.STATE_INITIAL)

    def set_state(self, state):
        initial_root = self._builder.get_object("state-initial")
        updating_root = self._builder.get_object("state-updating")
        error_root = self._builder.get_object("state-error")
        calendar_list_root = self._builder.get_object("state-calendar-list")
        refresh_button = self._builder.get_object("refresh-button")
        clean_start_button = self._builder.get_object("clean-start-button")
        clean_stop_button = self._builder.get_object("clean-stop-button")
        age_spinbutton = self._builder.get_object("age-spinbutton")

        initial_root.set_visible(state == self.STATE_INITIAL)
        updating_root.set_visible(state == self.STATE_UPDATING)
        error_root.set_visible(state == self.STATE_ERROR)
        calendar_list_root.set_visible(
            state in [self.STATE_CALENDAR_LIST, self.STATE_CLEANING]
        )

        refresh_button.set_visible(state == self.STATE_CALENDAR_LIST)
        clean_start_button.set_visible(state == self.STATE_CALENDAR_LIST)
        clean_stop_button.set_visible(state == self.STATE_CLEANING)
        age_spinbutton.set_sensitive(state == self.STATE_CALENDAR_LIST)

        self._column_checkbox.set_visible(state == self.STATE_CALENDAR_LIST)
        self._column_progress.set_visible(state == self.STATE_CLEANING)

    def set_error(self, title="", description="", detail=""):
        title_label = self._builder.get_object("error-title-label")
        description_label = self._builder.get_object("error-description-label")
        detail_label = self._builder.get_object("error-detail-label")
        more_expander = self._builder.get_object("error-more-expander")

        title_label.set_text(title)
        description_label.set_text(description)
        detail_label.set_text(detail)

        more_expander.set_visible(bool(detail))

    def _initialize_treeview(self):
        app = self.get_application()
        calendar_treeview = self._builder.get_object("calendar-treeview")
        calendar_treeview.set_model(app.calendar_store.gtk_list_store)

        # TODO
        def _toggle(widget, index):
            calendar = app.calendar_store.get(index)
            app.calendar_store.update(
                index, clean_enabled=not calendar["clean_enabled"]
            )

        # Color
        column = Gtk.TreeViewColumn(
            cell_renderer=Gtk.CellRendererText(),
            markup=app.calendar_store.FIELDS["calendar_color"]["id"],
        )
        column.set_expand(False)
        calendar_treeview.append_column(column)

        # Caldendar Name | Account Name
        column = Gtk.TreeViewColumn("Calendar")
        column.set_expand(True)
        calendar_name_renderer = Gtk.CellRendererText(weight=700)
        account_name_renderer = Gtk.CellRendererText(weight=300, scale=0.75)
        column.pack_start(calendar_name_renderer, True)
        column.pack_start(account_name_renderer, True)
        column.get_area().set_orientation(Gtk.Orientation.VERTICAL)
        column.add_attribute(
            calendar_name_renderer,
            "text",
            app.calendar_store.FIELDS["calendar_name"]["id"],
        )
        column.add_attribute(
            account_name_renderer,
            "text",
            app.calendar_store.FIELDS["account_name"]["id"],
        )
        calendar_treeview.append_column(column)

        # Event Count
        column = Gtk.TreeViewColumn(
            "Events",
            cell_renderer=Gtk.CellRendererText(),
            text=app.calendar_store.FIELDS["event_count"]["id"],
        )
        column.set_expand(True)
        calendar_treeview.append_column(column)

        # Clean Enabled
        renderer = Gtk.CellRendererToggle()
        renderer.connect("toggled", _toggle)
        self._column_checkbox = Gtk.TreeViewColumn(
            "Purge",
            cell_renderer=renderer,
            active=app.calendar_store.FIELDS["clean_enabled"]["id"],
        )
        self._column_checkbox.set_expand(False)
        calendar_treeview.append_column(self._column_checkbox)

        # Clean Progress
        self._column_progress = Gtk.TreeViewColumn(
            "Cleaning",
            cell_renderer=Gtk.CellRendererProgress(),
            value=app.calendar_store.FIELDS["clean_progress"]["id"],
            text=app.calendar_store.FIELDS["clean_progress_text"]["id"],
        )
        self._column_progress.set_expand(True)
        calendar_treeview.append_column(self._column_progress)
