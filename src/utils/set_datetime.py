from datetime import datetime, timezone


def set_timezone_now() -> datetime:
    return datetime.now().astimezone(timezone.utc)
