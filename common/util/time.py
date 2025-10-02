from datetime import datetime, timezone


def now(tz=timezone.utc):
    return datetime.now(tz=tz)
