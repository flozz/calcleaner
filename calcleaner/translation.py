import os
import locale
import gettext

from . import APPLICATION_ID
from . import data_helpers


if "LANG" not in os.environ:
    language, encoding = locale.getlocale()
    os.environ["LANG"] = language

translation = gettext.translation(
    APPLICATION_ID,
    localedir=data_helpers.find_data_path("locales"),
    fallback=True,
)

if hasattr(locale, "bindtextdomain"):
    locale.bindtextdomain(APPLICATION_ID, data_helpers.find_data_path("locales"))
else:
    print("W: Unable to bind text domaine")

gettext = translation.gettext
