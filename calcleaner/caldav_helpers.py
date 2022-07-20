from urllib.parse import urlparse
from datetime import datetime, timedelta

from caldav import DAVClient
from caldav.elements import ical


def fetch_calendars(url, username, password):
    with DAVClient(url, username=username, password=password) as dav_client:
        dav_principal = dav_client.principal()
        for calendar in dav_principal.calendars():
            color = calendar.get_properties([ical.CalendarColor()]).get(
                "{http://apple.com/ns/ical/}calendar-color", "#888888"
            )
            yield {
                "url": calendar.canonical_url,
                "name": calendar.name,
                "color": color,
                "event_count": len(calendar.events()),
            }


def clean_calendar(url, username, password, older_than_weeks=16):
    start_date = datetime(year=1900, month=1, day=1)
    end_date = datetime.now() - timedelta(weeks=older_than_weeks)

    with DAVClient(url, username=username, password=password) as dav_client:
        dav_principal = dav_client.principal()
        old_events = None

        for calendar in dav_principal.calendars():
            if calendar.canonical_url == url:
                old_events = calendar.date_search(start=start_date, end=end_date)
                break

        if old_events:
            cleaned_count = 0
            for event in old_events:
                cleaned_count += 1
                event.delete()
                yield (cleaned_count, len(old_events))
        else:
            return [(0, 0)]


def readable_account_url(url, username):
    return "@".join([username, urlparse(url).netloc])
