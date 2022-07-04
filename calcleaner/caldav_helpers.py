from caldav import DAVClient


def fetch_calendars(url, username, password):
    calendars = {}

    with DAVClient(url, username=username, password=password) as dav_client:
        dav_principal = dav_client.principal()
        for calendar in dav_principal.calendars():
            calendars[calendar.canonical_url] = {
                "name": calendar.name,
                "color": "#888888",  # TODO
                "event_count": len(calendar.events()),
            }

    return calendars
