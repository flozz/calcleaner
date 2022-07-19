from gi.repository import Gtk


class CalendarStore(object):

    # fmt: off
    FIELDS = {
        "account_name":   {"id": 0, "type": str,  "default": ""},
        "calendar_url":   {"id": 1, "type": str,  "default": ""},
        "calendar_name":  {"id": 2, "type": str,  "default": ""},
        "calendar_color": {"id": 3, "type": str,  "default": "#888888"},
        "event_count":    {"id": 4, "type": int,  "default": 0},
        "clean_enabled":  {"id": 5, "type": bool, "default": True},
        "clean_progress": {"id": 6, "type": int,  "default": 0},
    }
    # fmt: on

    gtk_list_store = None

    def __init__(self):
        store_fields = sorted(self.FIELDS.values(), key=lambda v: v["id"])
        self.gtk_list_store = Gtk.ListStore(*[f["type"] for f in store_fields])

    @property
    def length(self):
        """The length of the store."""
        return len(self.gtk_list_store)

    def append(self, **kwargs):
        """Appends a row to the store.

        :param **kwargs: The columns key/value of the row.

        :rtype: gtk.TreeIter
        :return: the iter of the inserted value.

        >>> store = CalendarStore()
        >>> store.length
        0
        >>> store.append(
        ...     account_name="user@example.org",
        ... )
        <Gtk.TreeIter object ...>
        >>> store.length
        1
        >>> store.append(foo="bar")
        Traceback (most recent call last):
            ...
        KeyError: "Invalid field 'foo'"
        """
        for key in kwargs:
            if key not in self.FIELDS:
                raise KeyError("Invalid field '%s'" % key)

        row = [None] * len(self.FIELDS)

        for key in self.FIELDS:
            field_info = self.FIELDS[key]
            row[field_info["id"]] = field_info["default"]

        iter_ = self.gtk_list_store.append(row)
        self.update(iter_, **kwargs)
        return iter_

    def clear(self):
        """Clears the store.

        >>> store = CalendarStore()
        >>> store.append()
        <Gtk.TreeIter object ...>
        >>> store.length
        1
        >>> store.clear()
        >>> store.length
        0
        """
        self.gtk_list_store.clear()

    def get(self, index_or_iter):
        """Get row data.

        :param int,gtk.TreeIter index_or_iter: The index of the row.

        :rtype: dict
        :returns: The row data (e.g. ``{"field_name": "value"}``.

        >>> store = CalendarStore()
        >>> store.append()
        <Gtk.TreeIter object ...>
        >>> store.get(0)
        {...}
        >>> store.get(1)
        Traceback (most recent call last):
            ...
        IndexError: ...
        """
        row = self.gtk_list_store[index_or_iter]
        result = {}

        for field_name, field_info in self.FIELDS.items():
            result[field_name] = row[field_info["id"]]

        return result

    def update(self, index_or_iter, **kwargs):
        """Updates a row.

        :param int,Gtk.TreeIter index_or_iter: The index of the row.
        :param **kwargs: The columns key/value of the row.

        >>> store = CalendarStore()
        >>> store.append(
        ...     calendar_name="Cal1",
        ... )
        <Gtk.TreeIter object ...>
        >>> store.get(0)["calendar_name"]
        'Cal1'
        >>> store.update(0, calendar_name="NewName")
        >>> store.get(0)["calendar_name"]
        'NewName'
        >>> store.update(0, foo="bar")
        Traceback (most recent call last):
            ...
        KeyError: "Invalid field 'foo'"
        >>> store.update(1, calendar_name="MyCalendar")
        Traceback (most recent call last):
            ...
        IndexError: ...
        """
        for key in kwargs:
            if key not in self.FIELDS:
                raise KeyError("Invalid field '%s'" % key)

        for key in kwargs:
            if key == "calendar_color":
                color_str = '<span fgcolor="%s">⬤</span>\n' % kwargs["calendar_color"]
                self._update_field(index_or_iter, key, color_str)
            else:
                self._update_field(index_or_iter, key, kwargs[key])

    def _update_field(self, index_or_iter, field_name, value):
        row = self.gtk_list_store[index_or_iter]
        row[self.FIELDS[field_name]["id"]] = value
