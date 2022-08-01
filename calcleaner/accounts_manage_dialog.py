from gi.repository import Gtk

from . import data_helpers


class AccountsManageDialog(object):
    def __init__(self, app, parent_window=None):
        self._app = app
        self._account_store = Gtk.ListStore(str)

        self._builder = Gtk.Builder()
        self._builder.add_from_file(
            data_helpers.find_data_path("ui/accounts-manage-dialog.glade")
        )
        self._builder.connect_signals(self)

        self._dialog = self._builder.get_object("account-manage-dialog")
        self._dialog.set_application(app)
        self._dialog.set_transient_for(parent_window)

        self._initialize_treeview()
        self._update_accounts()
        self._update_ui()

    def run(self):
        self._dialog.run()

    def get_selected_accounts_iter(self):
        accounts_treeview = self._builder.get_object("accounts-treeview")
        selection = accounts_treeview.get_selection()
        model = accounts_treeview.get_model()

        _, tree_paths = selection.get_selected_rows()
        return [model.get_iter(tree_path) for tree_path in tree_paths]

    def _initialize_treeview(self):
        accounts_treeview = self._builder.get_object("accounts-treeview")

        accounts_treeview.set_model(self._account_store)

        column = Gtk.TreeViewColumn(
            cell_renderer=Gtk.CellRendererText(),
            text=0,
        )
        accounts_treeview.append_column(column)

    def _update_accounts(self):
        self._account_store.clear()
        for account_name in self._app.accounts.list():
            self._account_store.append([account_name])

    def _update_ui(self):
        selected = self.get_selected_accounts_iter()

        remove_button = self._builder.get_object("remove-button")
        remove_button.set_sensitive(len(selected) > 0)

        edit_button = self._builder.get_object("edit-button")
        edit_button.set_sensitive(len(selected) == 1)

    def _on_close(self, *args):
        self._dialog.destroy()

    def _on_treeview_selection_changed(self, selection):
        self._update_ui()

    def _on_add_button_clicked(self, widget):
        self._app.add_account(update=False)
        self._update_accounts()

    def _on_remove_button_clicked(self, widget):
        selected = self.get_selected_accounts_iter()
        for iter_ in selected:
            account_name = self._account_store[iter_][0]
            self._app.accounts.remove(account_name)
        self._update_accounts()

    def _on_edit_button_clicked(self, widget):
        selected = self.get_selected_accounts_iter()
        account_name = self._account_store[selected[0]][0]
        self._app.edit_account(account_name)
        self._update_accounts()
