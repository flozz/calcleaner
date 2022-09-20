from gi.repository import Gtk
from gi.repository import Gdk


def load_gtk_custom_css(path):
    """Load custom GTK CSS from path.

    :param str path: Path to the CSS file.
    """
    css_provider = Gtk.CssProvider()
    css_provider.load_from_path(path)
    screen = Gdk.Screen.get_default()
    style_context = Gtk.StyleContext()
    style_context.add_provider_for_screen(
        screen,
        css_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_USER,
    )
