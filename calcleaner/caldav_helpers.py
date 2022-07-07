from urllib.parse import urlparse

from caldav import DAVClient
from caldav.elements import ical


def fetch_calendars(url, username, password):
    calendars = {}

    with DAVClient(url, username=username, password=password) as dav_client:
        dav_principal = dav_client.principal()
        for calendar in dav_principal.calendars():
            color = calendar.get_properties([ical.CalendarColor()]).get(
                "{http://apple.com/ns/ical/}calendar-color", "#888888"
            )
            calendars[calendar.canonical_url] = {
                "name": calendar.name,
                "color": color,
                "event_count": len(calendar.events()),
            }

    return calendars


def readable_account_url(url, username):
    return "@".join([username, urlparse(url).netloc])
